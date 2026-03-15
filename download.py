import kagglehub

# 데이터셋 다운로드 (자동으로 경로 지정됨)
path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")

print("데이터셋 저장 경로:", path)