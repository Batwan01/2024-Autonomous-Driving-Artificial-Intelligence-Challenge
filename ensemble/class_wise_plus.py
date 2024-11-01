import pandas as pd
import os
from mAP50_calculator import calculate_map50

# 두 개의 CSV 파일을 병합하고 특정 클래스(bus_warning)의 예측값을 추가하는 함수
def merge_bus_warning_values(csv1_path, csv2_path, output_path):
    # 첫 번째 CSV 파일 불러오기
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # bus_warning 클래스 ID 정의 (클래스 정의에 따라 인덱스가 다를 수 있음)
    BUS_WARNING_CLASS_ID = 13

    # 두 번째 CSV에서 bus_warning 값을 첫 번째 CSV에 병합
    for idx, row in df1.iterrows():
        prediction_string1 = row['PredictionString']
        prediction_string2_list = df2[df2['image_id'] == row['image_id']]['PredictionString'].tolist()

        # 두 번째 CSV에 해당 image_id가 없는 경우 건너뜀
        if not prediction_string2_list or pd.isna(prediction_string2_list[0]):
            continue

        prediction_string2 = prediction_string2_list[0]
        predictions1 = str(prediction_string1).split()
        predictions2 = str(prediction_string2).split()

        # 두 번째 CSV에서 bus_warning 클래스 예측만 필터링
        if len(predictions2) > 1:
            predictions2 = [predictions2[i:i + 6] for i in range(0, len(predictions2), 6)]
            bus_warning_predictions = [pred for pred in predictions2 if int(pred[0]) == BUS_WARNING_CLASS_ID]
        else:
            bus_warning_predictions = []

        # 첫 번째 CSV에서 예측값 파싱
        if len(predictions1) > 1:
            predictions1 = [predictions1[i:i + 6] for i in range(0, len(predictions1), 6)]
        else:
            predictions1 = []

        # 최종 PredictionString 생성 (원본 예측값에 bus_warning 예측값 추가)
        final_predictions = predictions1 + bus_warning_predictions
        df1.at[idx, 'PredictionString'] = ' '.join([' '.join(pred) for pred in final_predictions])

    # 결과 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df1.to_csv(output_path, index=False)
    print(f"Merged result saved to {output_path}")

if __name__ == "__main__":
    csv1_path = '/data/ephemeral/home/jiwan/2024-Autonomous-Driving-Artificial-Intelligence-Challenge/ensemble/output/csv/Co-DETR(Obj365, 3ep)_val.csv'
    csv2_path = '/data/ephemeral/home/jiwan/2024-Autonomous-Driving-Artificial-Intelligence-Challenge/ensemble/output/csv/co_dino_swin_l_o365_custom_2048_oversampling_val.csv'
    output_path = '/data/ephemeral/home/jiwan/2024-Autonomous-Driving-Artificial-Intelligence-Challenge/ensemble/output/csv/merged_bus_warning_plus.csv'

    # 두 번째 CSV에서 bus_warning 값을 첫 번째 CSV에 병합
    merge_bus_warning_values(csv1_path, csv2_path, output_path)
