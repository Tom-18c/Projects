import requests
import re
import inspect
import plotly.express as px

result_indef = []


# 循环输出键名
def OutPutKeyName(dict_indef, prefix_indef=""):
    # 格式化输出键名
    for count_var_1, loop_var_1 in enumerate(dict_indef.keys(), start=1):
        print(f"{prefix_indef}{count_var_1} ：{loop_var_1}")
    # （以列表形式）返回键名
    return list(dict_indef.keys())


# api调用步骤1-准备基本信息-接口地址
call_api_url_front = "https://api.github.com/search/repositories"
call_api_url_behind = "?q=language:python+sort:stars+stars:>80000"
call_api_url = f"{call_api_url_front}{call_api_url_behind}"

# api调用步骤1-准备基本信息-接口请求头
headers = {"Accept": "application/vnd.github.v3+json"}

# api调用步骤2-获取数据
get_r1 = requests.get(call_api_url, headers=headers)
# api调用步骤2-查看获取状态码（200表示成功、404表示失败）
print(f"响应状态码：{get_r1.status_code}，{"成功" if get_r1.status_code == 200 else "失败"}")

# api调用步骤3-处理数据-转化为dict
get_r1_dict = get_r1.json()

# api调用步骤3-处理数据-输出键名
key_name_list = OutPutKeyName(get_r1_dict, prefix_indef="第一层键")
print(f"满足条件的总仓库数：{get_r1_dict[key_name_list[0]]}")
print(f"响应数据包含仓库数：{len(get_r1_dict[key_name_list[2]])}")

# 输出仓库信息
for count_var_2, loop_var_2 in enumerate(get_r1_dict[key_name_list[2]], start=1):
    # print(loop_var_2.keys())
    print("==============================隔断符==============================")
    print(f"第{count_var_2}个仓库信息：")
    print(f"仓库名称：{loop_var_2["name"]}")
    print(f"仓库所有者：{loop_var_2["owner"]["login"]}")
    print(f"仓库star数：{loop_var_2["stargazers_count"]}")
    print(f"仓库创建时间：{loop_var_2["created_at"]}")
    print(f"仓库更新时间：{loop_var_2["updated_at"]}")
    print(f"仓库地址：{loop_var_2["html_url"]}")
    # print(f"仓库描述：{loop_var_2["description"]}")

dict_keys = [
    "id",
    "node_id",
    "name",
    "full_name",
    "private",
    "owner",
    "html_url",
    "description",
    "fork",
    "url",
    "forks_url",
    "keys_url",
    "collaborators_url",
    "teams_url",
    "hooks_url",
    "issue_events_url",
    "events_url",
    "assignees_url",
    "branches_url",
    "tags_url",
    "blobs_url",
    "git_tags_url",
    "git_refs_url",
    "trees_url",
    "statuses_url",
    "languages_url",
    "stargazers_url",
    "contributors_url",
    "subscribers_url",
    "subscription_url",
    "commits_url",
    "git_commits_url",
    "comments_url",
    "issue_comment_url",
    "contents_url",
    "compare_url",
    "merges_url",
    "archive_url",
    "downloads_url",
    "issues_url",
    "pulls_url",
    "milestones_url",
    "notifications_url",
    "labels_url",
    "releases_url",
    "deployments_url",
    "created_at",
    "updated_at",
    "pushed_at",
    "git_url",
    "ssh_url",
    "clone_url",
    "svn_url",
    "homepage",
    "size",
    "stargazers_count",
    "watchers_count",
    "language",
    "has_issues",
    "has_projects",
    "has_downloads",
    "has_wiki",
    "has_pages",
    "has_discussions",
    "forks_count",
    "mirror_url",
    "archived",
    "disabled",
    "open_issues_count",
    "license",
    "allow_forking",
    "is_template",
    "web_commit_signoff_required",
    "has_pull_requests",
    "pull_request_creation_policy",
    "topics",
    "visibility",
    "forks",
    "open_issues",
    "watchers",
    "default_branch",
    "score",
]
