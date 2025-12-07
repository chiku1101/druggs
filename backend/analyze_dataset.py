import pandas as pd

df = pd.read_csv('services/medicine_dataset.csv')

print("=" * 60)
print("📊 YOUR DATASET - WHAT YOU CAN SEARCH")
print("=" * 60)

print("\n✅ ALL AVAILABLE INDICATIONS (Conditions):")
print("-" * 60)
indications = sorted(df['Indication'].unique())
for ind in indications:
    count = len(df[df['Indication'] == ind])
    print(f"  • {ind} ({count} drugs)")

print("\n\n✅ SAMPLE DRUGS FOR EACH INDICATION:")
print("-" * 60)
for ind in indications:
    drugs = df[df['Indication'] == ind]['Name'].unique()[:5]
    print(f"\n{ind}:")
    print(f"  {', '.join(drugs)}")

print("\n\n✅ POPULAR DRUG NAMES (Most Common):")
print("-" * 60)
top_drugs = df['Name'].value_counts().head(20)
for drug, count in top_drugs.items():
    print(f"  • {drug} ({count} records)")

print("\n\n✅ ALL CATEGORIES:")
print("-" * 60)
categories = sorted(df['Category'].unique())
for cat in categories:
    count = len(df[df['Category'] == cat])
    print(f"  • {cat} ({count} drugs)")

print("\n" + "=" * 60)

