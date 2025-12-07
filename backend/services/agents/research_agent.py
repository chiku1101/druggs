"""
Research Agent - Fetches research papers from PubMed
"""

from .base_agent import BaseAgent
from typing import Dict, Any, List
import aiohttp
import json


class ResearchAgent(BaseAgent):
    """
    Fetches research papers from PubMed API
    """
    
    def __init__(self):
        super().__init__("ResearchAgent")
        self.pubmed_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.timeout = 20
        
    async def execute(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Fetch research papers related to drug repurposing
        """
        papers = []
        
        # Search for relevant papers
        search_query = f'"{drug_name}" AND "{target_condition}" AND repurposing'
        
        try:
            papers = await self._search_pubmed(search_query)
        except Exception as e:
            print(f"PubMed search failed: {e}, trying alternative search")
            # Fallback search
            search_query = f'"{drug_name}" AND "{target_condition}"'
            try:
                papers = await self._search_pubmed(search_query)
            except:
                pass
        
        return {
            "research_papers": papers,
            "total_papers_found": len(papers),
            "search_query": search_query
        }
    
    async def _search_pubmed(self, query: str) -> List[Dict[str, Any]]:
        """
        Search PubMed for papers using XML parsing
        """
        papers = []
        
        # Step 1: Search for relevant PMIDs
        search_url = f"{self.pubmed_base_url}/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": 10,  # Get top 10 results
            "rettype": "xml"  # Changed to XML (default)
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(search_url, params=search_params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        xml_text = await resp.text()
                        pmids = self._parse_esearch_xml(xml_text)
                        
                        if pmids:
                            # Step 2: Fetch paper details
                            papers = await self._fetch_paper_details(session, pmids)
            except Exception as e:
                print(f"Error searching PubMed: {e}")
        
        return papers
    
    def _parse_esearch_xml(self, xml_text: str) -> List[str]:
        """
        Parse XML response from PubMed esearch
        """
        import xml.etree.ElementTree as ET
        pmids = []
        
        try:
            root = ET.fromstring(xml_text)
            # Find all Id elements (PMIDs)
            for id_elem in root.findall('.//Id'):
                if id_elem.text:
                    pmids.append(id_elem.text)
        except Exception as e:
            print(f"Error parsing PubMed XML: {e}")
        
        return pmids
    
    async def _fetch_paper_details(self, session: aiohttp.ClientSession, pmids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch detailed information about papers using XML parsing
        """
        papers = []
        
        fetch_url = f"{self.pubmed_base_url}/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids[:5]),  # Limit to 5 papers
            "rettype": "xml"  # XML format
        }
        
        try:
            async with session.get(fetch_url, params=fetch_params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    xml_text = await resp.text()
                    papers = self._parse_efetch_xml(xml_text)
        except Exception as e:
            print(f"Error fetching paper details: {e}")
        
        return papers
    
    def _parse_efetch_xml(self, xml_text: str) -> List[Dict[str, Any]]:
        """
        Parse XML response from PubMed efetch and extract article information
        """
        import xml.etree.ElementTree as ET
        papers = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # Find all PubmedArticle elements
            for article in root.findall('.//PubmedArticle'):
                paper = self._extract_article_from_xml(article)
                if paper:
                    papers.append(paper)
        except Exception as e:
            print(f"Error parsing efetch XML: {e}")
        
        return papers
    
    def _extract_article_from_xml(self, article_elem) -> Dict[str, Any]:
        """
        Extract article information from XML element
        """
        import xml.etree.ElementTree as ET
        
        try:
            # Extract title
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "Unknown Title"
            
            # Extract authors
            authors = []
            for author_elem in article_elem.findall('.//Author'):
                last_name = author_elem.find('LastName')
                first_name = author_elem.find('ForeName')
                
                author_name = ""
                if last_name is not None and last_name.text:
                    author_name = last_name.text
                if first_name is not None and first_name.text:
                    author_name = first_name.text[0] + ". " + author_name
                
                if author_name:
                    authors.append(author_name)
            
            authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
            
            # Extract journal
            journal_elem = article_elem.find('.//Title')  # Journal title
            journal = journal_elem.text if journal_elem is not None else "Journal Unknown"
            
            # Extract year
            year_elem = article_elem.find('.//Year')
            year = year_elem.text if year_elem is not None else "2023"
            
            # Extract PMID
            pmid_elem = article_elem.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else ""
            
            # Extract abstract
            abstract_elem = article_elem.find('.//AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else ""
            
            # Calculate relevance
            relevance = self._calculate_relevance(title, abstract)
            
            return {
                "title": title,
                "authors": authors_str if authors_str else "Unknown Authors",
                "journal": journal,
                "year": int(year) if year.isdigit() else 2023,
                "relevance": relevance,
                "summary": abstract[:500] if abstract else "Abstract not available",
                "pmid": pmid,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""
            }
        except Exception as e:
            print(f"Error extracting article: {e}")
            return None
    
    def _calculate_relevance(self, title: str, abstract: str) -> int:
        """
        Calculate relevance score (0-100)
        """
        score = 50
        text = (title + " " + abstract).lower()
        
        # Keyword matching
        keywords = {
            "repurposing": 15,
            "repurpose": 15,
            "indication": 10,
            "efficacy": 10,
            "clinical trial": 15,
            "mechanism": 5,
            "therapy": 5
        }
        
        for keyword, points in keywords.items():
            if keyword in text:
                score += points
        
        return min(100, max(40, score))
