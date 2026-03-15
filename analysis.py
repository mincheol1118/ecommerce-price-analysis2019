import pandas as pd
import os

base_path = r"C:\Users\minch\.cache\kagglehub\datasets\mkechinov\ecommerce-behavior-data-from-multi-category-store\versions\8"
# 파일명을 2019-Nov.csv로 변경해서 돌려보세요
file_path = os.path.join(base_path, "2019-Nov.csv")

# 특정 구간의 브랜드/카테고리를 담을 딕셔너리
target_info = {
    '$950-1000': {'categories': [], 'brands': []},
    '$700-750': {'categories': [], 'brands': []},
    '$250-300': {'categories': [], 'brands': []}
}

print("11월 데이터 전수 분석 및 구간별 정체 파악 시작...")

for i, chunk in enumerate(pd.read_csv(file_path, chunksize=1000000)):
    chunk = chunk[(chunk['price'] > 0) & (chunk['event_type'] == 'purchase')].copy()
    
    # 가격 구간 나누기
    bins = list(range(0, 1050, 50)) + [float('inf')]
    labels = [f"${i}-{i+50}" for i in range(0, 1000, 50)] + ["$1000+"]
    chunk['price_range'] = pd.cut(chunk['price'], bins=bins, labels=labels)
    
    # 우리가 궁금한 구간의 데이터만 추출해서 리스트에 보관
    for r in target_info.keys():
        subset = chunk[chunk['price_range'] == r]
        target_info[r]['categories'].append(subset['category_code'].fillna('unknown'))
        target_info[r]['brands'].append(subset['brand'].fillna('unknown'))

    if (i + 1) % 10 == 0:
        print(f"{(i + 1)}백만 행 처리 중...")

print("\n" + "="*50)
print("전수 분석 기반 구간별 핵심 정체 (Final Reveal)")
print("="*50)

for r in target_info.keys():
    print(f"\n[구간: {r}]")
    all_cats = pd.concat(target_info[r]['categories'])
    all_brands = pd.concat(target_info[r]['brands'])
    
    print("- Top 3 Categories:")
    print(all_cats.value_counts().head(3))
    print("- Top 3 Brands:")
    print(all_brands.value_counts().head(3))