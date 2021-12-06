"""
    read openapi json file and export data
"""
import json
import excel.write as excel
from pprint import pprint as pp

if __name__ == '__main__':
    print("export start")

file_path = "../json/openapi.json"

# summary data
summary = []

with open(file_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

    info = json_data['info']
    paths = json_data['paths']
    components = json_data['components']

    print("title : ", info['title'])
    print("version : ", info['version'])
    # print("api count : ", len(paths))
    api_count = 0

    # 대메뉴 | 중메뉴 | 소메뉴 | API URI | methods
    print("대메뉴 |  중메뉴 |  소메뉴  |   API URI     | methods ")

    for key, value in paths.items():
        if 'root' in key:
            continue

        api_count += 1
        api_uri = key
        # print(f'key= {key}', f'value= {value}')
        # print(f'key= {key}')
        # pp(value)

        # depth는 3단계까지만...
        depth = ['']*3
        uri_depth = api_uri.split("/")
        methods = ', '.join(list(value.keys()))

        for idx, uri_value in enumerate(uri_depth):
            if 1 < idx < 5:
                try:
                    depth[idx-2] = uri_value
                except:
                    depth[idx-2] = ''

            # print(f"depth list : {depth}")

        # print("\nmethods : ", ', '.join(list(value.keys())))
        # print(f'{depth[0]} | {depth[1]} | {depth[2]} | {key} | {methods}')
        summary.append(f'{depth[0]} | {depth[1]} | {depth[2]} | {key} | {methods}')

print(summary)

# Call create excel file function
save_path = "../data/api_summary.xlsx"
excel.create_excel_file(summary, save_path)


