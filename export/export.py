"""
    read openapi json file and export data
"""
import json
from pprint import pprint as pp
import excel.write as excel
import model.api_info as api_info
import model.request as request
import model.response as response
import model.schema as schema

file_path = "../json/openapi.json"

summary = []  # summary data
sheets_info = dict()  # {[],[]...}


def set_api_info(items: dict):

    for method, detail in items:
        # print("sheet name : ", detail["tags"][-1])

        # summary
        info_summary = detail["summary"]

        info_desc = None
        security = None
        request_info = None
        param_info = None
        responses = None

        # description
        if detail.get('description') is not None:
            info_desc = detail["description"]

        # security (securitySchemas/OAuth2PasswordBearerWithCookie에 상세 정의 있음)
        if detail.get("security") is not None:
            security_dict = detail["security"][0]
            if len(security_dict) > 0:
                # 일단 key만 가져옴
                security = list(security_dict.keys())[0]

        # request body
        if "requestBody" in detail.keys():
            request_info = get_requestInfo(detail["requestBody"])

        # parameters ( 'in': 'query' / 'in': 'path')
        if "parameters" in detail.keys():
            param_info = get_parameters(detail["parameters"])

        # responses (list)
        if "responses" in detail.keys():
            # print(detail["responses"])
            responses = get_responses(detail["responses"])

        # set api info
        sheet_info = api_info.ApiInfo(info_summary, info_desc, method, key, security, request_info, param_info, responses)

        # add sheet list
        if sheet_name in sheets_info:
            sheets_info[sheet_name].append(sheet_info)


# return ref schema value
def get_ref_value(ref: str):
    schema_path = ref.split("/")
    return components[schema_path[2]][schema_path[3]]


#  p_name : schema name
#  p_value : schema info
#  p_list : 최종 schema info list
def get_properties(p_name: str, in_value: dict, p_list: list):

    # key에 $ref 가 있는 경우 : Object 형식
    if "$ref" in in_value.keys():
        ref_value = dict()
        ref_value["name"] = in_value["name"] if "name" in in_value.keys() else p_name
        ref_value["title"] = in_value["title"] if "title" in in_value.keys() else in_value["$ref"].split("/")[-1]
        ref_value["type"] = "object"

        p_list.append(ref_value)
        get_properties(p_name, get_ref_value(in_value["$ref"]), p_list)

    # key에 items 가 있는 경우 : Array 형식(내부객체는 type 으로 정의)
    elif "items" in in_value.keys():
        ref_value = dict()
        ref_value["name"] = in_value["name"] if "name" in in_value.keys() else p_name
        ref_value["title"] = in_value["title"] if "title" in in_value.keys() else None
        ref_value["type"] = "array"

        if "$ref" in in_value["items"].keys():
            p_list.append(ref_value)
            get_properties(f'{p_name}[]', get_ref_value(in_value["items"]["$ref"]), p_list)

        elif "type" in in_value["items"].keys():
            ref_value["type"] = f'array of {in_value["items"]["type"]}s'
            # (e.g) array of strings <binary>
            if "format" in in_value["items"].keys():
                ref_value["type"] += f' <{in_value["items"]["format"]}>'
            p_list.append(ref_value)
        else:
            ref_value["type"] = "array of any"
            p_list.append(ref_value)

    elif "properties" in in_value.keys():
        for prop_key, prop_value in in_value["properties"].items():
            get_properties(f'{p_name}.{prop_key}', prop_value, p_list)

    else:
        in_value["name"] = in_value["name"] if "name" in in_value.keys() else p_name
        p_list.append(in_value)

    return p_list


def get_requestInfo(requestBody):
    content_type = list(requestBody["content"].keys())[0]
    schema_ref = requestBody["content"][content_type]["schema"]["$ref"]

    schema_value = get_ref_value(schema_ref)
    # print(f'[{method}]', key)

    schema_list = []  # schema class list
    required_list = []
    if "required" in schema_value.keys():
        required_list = schema_value["required"]

    for p_name, p_value in schema_value["properties"].items():

        prop_list = get_properties(p_name, p_value, list())

        # schema class
        for prop_info in prop_list:
            schema_info = schema.ReqSchema(p_name, None, None, None, None, None)

            # name, title, type, description , default
            schema_info.name = prop_info['name'] if "name" in prop_info.keys() else p_name
            schema_info.title = prop_info["title"] if "title" in prop_info.keys() else None
            schema_info.type = prop_info["type"] if "type" in prop_info.keys() else None
            schema_info.default = prop_info["default"] if "default" in prop_info.keys() else None
            schema_info.description = prop_info["description"] if "description" in prop_info.keys() else None

            # add required
            if p_name in required_list:
                schema_info.required = "required"

            # schema_list : 최종 request 테이블
            schema_list.append(schema_info)

    return request.RequestInfo(content_type, requestBody["required"], schema_list)


def get_parameters(parameters):
    param_list = []
    for parameter in parameters:
        schema_info = schema.ParamSchema(parameter["name"], None, parameter["in"], parameter["required"], None,
                                         None, None)

        param_schema = parameter["schema"]
        schema_info.title = param_schema["title"] if "title" in param_schema.keys() else None
        schema_info.type = param_schema["type"] if "type" in param_schema.keys() else None
        schema_info.default = param_schema["default"] if "default" in param_schema.keys() else None
        schema_info.description = param_schema["description"] if "description" in param_schema.keys() else None

        param_list.append(schema_info)

    return param_list


def get_responses(responses):
    res_list = []   # response class list

    for code, res_info in responses.items():
        content_type = list(res_info["content"].keys())[0]
        schema_value = None
        schema_list = []  # schema class list

        if '$ref' in res_info["content"][content_type]["schema"]:
            schema_ref = res_info["content"][content_type]["schema"]["$ref"]
            schema_value = get_ref_value(schema_ref)
            for p_name, p_value in schema_value["properties"].items():

                prop_list = get_properties(p_name, p_value, list())

                # schema class
                for prop_info in prop_list:
                    schema_info = schema.ReqSchema(p_name, None, None, None, None, None)

                    # name, title, type, description , default
                    schema_info.name = prop_info['name'] if "name" in prop_info.keys() else p_name
                    schema_info.title = prop_info["title"] if "title" in prop_info.keys() else None
                    schema_info.type = prop_info["type"] if "type" in prop_info.keys() else None
                    schema_info.default = prop_info["default"] if "default" in prop_info.keys() else None
                    schema_info.description = prop_info["description"] if "description" in prop_info.keys() else None

                    schema_list.append(schema_info)

            res_list.append(response.ResponseInfo(code, content_type, res_info["description"], schema_list))

    return res_list


with open(file_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

    info = json_data['info']
    paths = json_data['paths']
    components = json_data['components']

    print("title : ", info['title'])
    print("version : ", info['version'])
    # print("api count : ", len(paths))
    api_count = 0

    for key, value in paths.items():
        if 'root' in key:
            continue

        api_count += 1
        api_uri = key

        # depth는 3단계까지만...
        depth = [''] * 3
        uri_depth = api_uri.split("/")
        methods = ', '.join(list(value.keys()))

        for idx, uri_value in enumerate(uri_depth):
            if 1 < idx < 5:
                try:
                    depth[idx - 2] = uri_value
                except:
                    depth[idx - 2] = ''

        sheet_name = depth[0]
        summary.append(f'{sheet_name} | {depth[1]} | {depth[2]} | {key} | {methods}')

        # set sheets dict
        if sheet_name not in sheets_info:
            sheets_info[sheet_name] = []

        # api 정보를 sheets에 채우기
        set_api_info(value.items())

        # print(f'key= {key}, value= {value}')

# Call create excel file function
save_path = "../data/api_summary.xlsx"
excel.create_excel_file(summary, sheets_info, save_path)


if __name__ == '__main__':
    print("export start")
