import json
import csv
from collections import defaultdict

def convert_coco_to_pascal_voc(coco_file, output_csv):
    # COCO JSON 파일 읽기
    with open(coco_file, 'r') as f:
        coco_data = json.load(f)

    # 이미지 ID를 키로 사용하여 주석 정보를 저장할 딕셔너리 생성
    image_annotations = defaultdict(list)

    # 주석 정보 처리
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        bbox = annotation['bbox']
        x, y, w, h = bbox
        x_min, y_min, x_max, y_max = x, y, x + w, y + h

        # Pascal VOC 형식으로 변환
        pascal_voc_annotation = f"{category_id} 1.0 {x_min} {y_min} {x_max} {y_max}"
        image_annotations[image_id].append(pascal_voc_annotation)

    # 이미지 정보를 리스트로 변환하고 파일명(숫자)으로 정렬
    image_info = []
    for image in coco_data['images']:
        file_name = image['file_name'].split('/')[-1]  # 파일 이름만 추출
        image_id = image['id']
        annotations = image_annotations[image_id]
        prediction_string = ' '.join(annotations)
        # 파일명에서 확장자를 제외한 숫자 부분을 추출하여 정수로 변환
        image_number = int(file_name.split('.')[0])
        image_info.append((image_number, file_name, prediction_string))

    # 이미지 번호로 정렬
    image_info.sort(key=lambda x: x[0])

    # CSV 파일 작성
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PredictionString', 'image_id'])

        for _, file_name, prediction_string in image_info:
            writer.writerow([prediction_string, file_name])

    print(f"CSV 파일이 생성되었습니다: {output_csv}")

# 스크립트 실행
coco_file = '../tld_db/json/val_coco.json'
output_csv = 'val_ground_truth.csv'
convert_coco_to_pascal_voc(coco_file, output_csv)