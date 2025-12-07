"""
Report Generator - Creates PDF reports for drug repurposing analysis
"""

from typing import Dict, Any
from datetime import datetime
import json
import os


class ReportGenerator:
    """
    Generates comprehensive PDF reports from analysis results
    """
    
    def __init__(self):
        self.report_dir = "./reports"
        self._ensure_report_dir()
    
    def _ensure_report_dir(self):
        """Ensure reports directory exists"""
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_pdf_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate PDF report from analysis data
        Uses ReportLab for PDF generation
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.colors import HexColor, grey
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        except ImportError:
            return {
                "success": False,
                "error": "ReportLab not installed. Install with: pip install reportlab",
                "message": "PDF generation requires ReportLab. Using JSON export instead."
            }
        
        # Generate filename
        drug = analysis_data.get("drug_name", "Drug").replace(" ", "_")
        condition = analysis_data.get("target_condition", "Condition").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/Drug_Repurposing_Report_{drug}_{condition}_{timestamp}.pdf"
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(filename, pagesize=letter,
                                  rightMargin=0.75*inch, leftMargin=0.75*inch,
                                  topMargin=0.75*inch, bottomMargin=0.75*inch)
            
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=HexColor('#1f4788'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=HexColor('#2e5c8a'),
                spaceAfter=12,
                spaceBefore=12,
                borderPadding=5
            )
            
            # Title Section
            story.append(Paragraph("Drug Repurposing Analysis Report", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Executive Summary
            drug_name = analysis_data.get("drug_name", "Unknown")
            target_condition = analysis_data.get("target_condition", "Unknown")
            verdict = analysis_data.get("verdict", "Unknown")
            score = analysis_data.get("repurposeability_score", 0)
            
            summary_data = [
                ["Drug Name:", drug_name],
                ["Target Condition:", target_condition],
                ["Case Type:", analysis_data.get("case_type", "Unknown").replace("_", " ").title()],
                ["Verdict:", f"{verdict} (Score: {score}/100)"],
                ["Confidence:", f"{analysis_data.get('confidence', 0)*100:.0f}%"],
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 3.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8eef5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1f4788')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
            ]))
            
            story.append(Paragraph("Executive Summary", heading_style))
            story.append(summary_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Recommendation
            recommendation = analysis_data.get("recommendation", "")
            story.append(Paragraph("Recommendation", heading_style))
            story.append(Paragraph(recommendation, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Score Breakdown
            story.append(Paragraph("Repurposeability Score Breakdown", heading_style))
            score_breakdown = analysis_data.get("score_breakdown", {})
            scores_data = [["Category", "Score"]]
            for category, score_val in score_breakdown.items():
                category_name = category.replace("_score", "").replace("_", " ").title()
                scores_data.append([category_name, f"{score_val}/100"])
            
            scores_table = Table(scores_data, colWidths=[3.25*inch, 1.25*inch])
            scores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('white')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f0f4f8'), HexColor('white')]),
            ]))
            
            story.append(scores_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Reasoning
            story.append(Paragraph("Reasoning", heading_style))
            reasoning = analysis_data.get("reasoning", [])
            for item in reasoning:
                story.append(Paragraph(f"• {item}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Risk Factors
            risk_factors = analysis_data.get("risk_factors", [])
            if risk_factors:
                story.append(PageBreak())
                story.append(Paragraph("Risk Factors", heading_style))
                
                for risk in risk_factors:
                    factor = risk.get("factor", "Unknown")
                    severity = risk.get("severity", "Unknown")
                    mitigation = risk.get("mitigation", "")
                    
                    risk_text = f"<b>{factor}</b> [Severity: {severity}]<br/>"
                    risk_text += f"Mitigation: {mitigation}"
                    story.append(Paragraph(risk_text, styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
            
            # Clinical Trials
            trials = analysis_data.get("clinical_trials", [])
            if trials:
                story.append(PageBreak())
                story.append(Paragraph("Clinical Trials", heading_style))
                
                trials_data = [["Trial ID", "Title", "Status", "Phase"]]
                for trial in trials[:5]:  # Show top 5
                    trials_data.append([
                        trial.get("id", "N/A")[:20],
                        trial.get("title", "")[:40],
                        trial.get("status", ""),
                        trial.get("phase", "")
                    ])
                
                trials_table = Table(trials_data, colWidths=[1*inch, 2.5*inch, 1.2*inch, 1*inch])
                trials_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2e5c8a')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('white')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f0f4f8'), HexColor('white')]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                story.append(trials_table)
            
            # Market Feasibility
            market = analysis_data.get("market_feasibility", {})
            if market:
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph("Market Feasibility", heading_style))
                
                market_data = [
                    ["Market Size:", market.get("market_size", "N/A")],
                    ["Growth Rate:", market.get("growth_rate", "N/A")],
                    ["Competition:", market.get("competition", "N/A")],
                    ["Timeline to Commercialization:", market.get("timeline", "N/A")],
                ]
                
                market_table = Table(market_data, colWidths=[2*inch, 3.5*inch])
                market_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8eef5')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
                ]))
                
                story.append(market_table)
            
            # Regulatory Info
            regulatory = analysis_data.get("regulatory_info", {})
            if regulatory:
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph("Regulatory Status", heading_style))
                
                fda_status = regulatory.get("fda_status", {})
                pathway = regulatory.get("regulatory_pathway", {})
                
                regulatory_text = f"<b>FDA Status:</b> "
                if fda_status.get("approved"):
                    regulatory_text += f"Approved for {fda_status.get('indication', 'other indications')}<br/>"
                else:
                    regulatory_text += "Not yet approved for this indication<br/>"
                
                regulatory_text += f"<b>Regulatory Pathway:</b> {pathway.get('pathway', 'N/A')}<br/>"
                regulatory_text += f"<b>Estimated Timeline:</b> {pathway.get('timeline', 'N/A')}<br/>"
                regulatory_text += f"<b>Estimated Cost:</b> {pathway.get('estimated_cost', 'N/A')}<br/>"
                
                story.append(Paragraph(regulatory_text, styles['Normal']))
            
            # Next Steps
            next_steps = analysis_data.get("next_steps", [])
            if next_steps:
                story.append(PageBreak())
                story.append(Paragraph("Recommended Next Steps", heading_style))
                for i, step in enumerate(next_steps, 1):
                    story.append(Paragraph(step, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            
            # Footer
            story.append(Spacer(1, 0.3*inch))
            timestamp_text = f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            story.append(Paragraph(timestamp_text, ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=grey,
                alignment=TA_CENTER
            )))
            
            # Build PDF
            doc.build(story)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": os.path.abspath(filename),
                "message": f"PDF report generated successfully: {filename}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate PDF report"
            }
    
    def generate_json_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate JSON report (always works, no dependencies)
        """
        # Generate filename
        drug = analysis_data.get("drug_name", "Drug").replace(" ", "_")
        condition = analysis_data.get("target_condition", "Condition").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/Drug_Repurposing_Report_{drug}_{condition}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(analysis_data, f, indent=2, default=str)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": os.path.abspath(filename),
                "message": f"JSON report generated successfully: {filename}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate JSON report"
            }
    
    def generate_report(self, analysis_data: Dict[str, Any], format: str = "pdf") -> Dict[str, Any]:
        """
        Generate report in specified format (pdf or json)
        Falls back to JSON if PDF fails
        """
        if format.lower() == "pdf":
            result = self.generate_pdf_report(analysis_data)
            
            # Fallback to JSON if PDF fails
            if not result.get("success"):
                print(f"PDF generation failed: {result.get('error')}, falling back to JSON")
                return self.generate_json_report(analysis_data)
            
            return result
        
        else:
            return self.generate_json_report(analysis_data)
