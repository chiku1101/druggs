# 🔍 SEARCH GUIDE - What You Can Search in Your Dataset

Based on your **medicine_dataset.csv** with **50,002 records**, here's what you can search:

---

## ✅ **TARGET CONDITIONS (Indications) - 8 Available:**

You can search for these **8 conditions** in the "Target Condition" field:

1. **Depression** (6,173 drugs available)
2. **Diabetes** (6,171 drugs available)
3. **Fever** (6,246 drugs available)
4. **Fungus** (6,294 drugs available)
5. **Infection** (6,393 drugs available)
6. **Pain** (6,163 drugs available)
7. **Virus** (6,292 drugs available)
8. **Wound** (6,268 drugs available)

---

## 💊 **DRUG NAMES - Examples You Can Search:**

### **Most Popular Drugs (Best to Search):**

1. **Metostatin** (860 records)
2. **Dolomet** (837 records)
3. **Metophen** (832 records)
4. **Dolonazole** (827 records)
5. **Acetomycin** (825 records)
6. **Dolocillin** (819 records)
7. **Dextronazole** (817 records)
8. **Dextromet** (813 records)
9. **Ibupromycin** (813 records)
10. **Metomet** (811 records)

### **Other Common Drugs:**

- **Acetocillin**, **Acetomet**, **Clarinazole**, **Cefmet**
- **Amoxivir**, **Clarivir**, **Acetovir**, **Claristatin**
- **Dextromycin**, **Ibuprocillin**, **Amoxicillin**
- **Metovir**, **Dolophen**, **Clariphen**, **Metoprofen**

---

## 🎯 **EXAMPLE SEARCHES THAT WILL WORK:**

### **Example 1:**
```
Drug Name: Metostatin
Target Condition: Diabetes
```
✅ **Will work!** - Metostatin has 860 records, many for Diabetes

### **Example 2:**
```
Drug Name: Dolomet
Target Condition: Infection
```
✅ **Will work!** - Dolomet has 837 records, many for Infection

### **Example 3:**
```
Drug Name: Amoxicillin
Target Condition: Wound
```
✅ **Will work!** - Amoxicillin is in your dataset for Wound

### **Example 4:**
```
Drug Name: Ibuprocillin
Target Condition: Pain
```
✅ **Will work!** - Ibuprocillin is in your dataset

### **Example 5:**
```
Drug Name: Cefmet
Target Condition: Depression
```
✅ **Will work!** - Cefmet has 806 records, many for Depression

---

## 📊 **DRUG CATEGORIES (8 Types):**

Your dataset has these drug categories:

1. **Analgesic** (6,340 drugs) - Pain relievers
2. **Antibiotic** (6,066 drugs) - Anti-bacterial
3. **Antidepressant** (6,354 drugs) - For depression
4. **Antidiabetic** (6,171 drugs) - For diabetes
5. **Antifungal** (6,289 drugs) - Anti-fungal
6. **Antipyretic** (6,280 drugs) - Fever reducers
7. **Antiseptic** (6,315 drugs) - Wound care
8. **Antiviral** (6,185 drugs) - Anti-viral

---

## 🎨 **UPDATE YOUR FRONTEND PLACEHOLDERS:**

### **Current Placeholders (Replace These):**
```
Drug Name: "e.g., Metformin, Aspirin, Sildenafil..."
Target Condition: "e.g., Cancer, PCOS, Cardiovascular Disease..."
```

### **New Placeholders (Based on Your Dataset):**
```
Drug Name: "e.g., Metostatin, Dolomet, Amoxicillin, Ibuprocillin..."
Target Condition: "e.g., Diabetes, Infection, Pain, Depression, Fever..."
```

---

## 🔍 **SEARCH TIPS:**

### ✅ **What Works:**
- **Exact drug names** from your CSV (e.g., "Metostatin", "Dolomet")
- **Any of the 8 indications** (Depression, Diabetes, Fever, Fungus, Infection, Pain, Virus, Wound)
- **Fuzzy matching** - Close spellings will work too!

### ❌ **What Won't Work:**
- Real-world drugs NOT in your CSV (e.g., "Metformin", "Aspirin" - these aren't in your dataset)
- Conditions NOT in your CSV (e.g., "Cancer", "PCOS" - these aren't in your dataset)

---

## 📝 **RECOMMENDED SEARCH EXAMPLES:**

### **High Success Rate Searches:**

1. **Metostatin + Diabetes** ⭐⭐⭐⭐⭐
   - 860 records for Metostatin
   - Many for Diabetes

2. **Dolomet + Infection** ⭐⭐⭐⭐⭐
   - 837 records for Dolomet
   - Many for Infection

3. **Amoxicillin + Wound** ⭐⭐⭐⭐
   - Amoxicillin in dataset
   - Used for Wound

4. **Ibuprocillin + Pain** ⭐⭐⭐⭐
   - Ibuprocillin in dataset
   - Used for Pain

5. **Cefmet + Depression** ⭐⭐⭐⭐
   - 806 records for Cefmet
   - Many for Depression

---

## 🎯 **QUICK REFERENCE:**

| Drug Name | Best For Condition | Records |
|-----------|-------------------|---------|
| Metostatin | Diabetes, Fever | 860 |
| Dolomet | Infection, Diabetes | 837 |
| Metophen | Fever, Virus | 832 |
| Dolonazole | Fungus, Pain | 827 |
| Acetomycin | Wound, Virus | 825 |
| Dolocillin | Diabetes, Infection | 819 |
| Amoxicillin | Wound, Fungus | Multiple |
| Ibuprocillin | Infection, Pain | Multiple |

---

## 💡 **PRO TIP:**

Since your dataset has **fuzzy matching**, you can search with:
- Partial names (e.g., "Met" will find "Metostatin", "Metophen")
- Close spellings (e.g., "Amox" will find "Amoxicillin", "Amoxivir")
- The system will find the closest match!

---

## 🚀 **READY TO TEST:**

Try these searches in your frontend:

1. **Metostatin** + **Diabetes**
2. **Dolomet** + **Infection**  
3. **Amoxicillin** + **Wound**
4. **Ibuprocillin** + **Pain**
5. **Cefmet** + **Depression**

All of these will return **GENUINE data from your CSV dataset!** 🎉

---

**Your dataset is ready! Use any of the 8 indications and any drug name from your CSV!** 📊✨

