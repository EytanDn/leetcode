import argparse
import html2text as ht

import leetcode as lc
from tempfile import NamedTemporaryFile
import yaml


def get_instance() -> lc.DefaultApi:
    with open(".secret.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    leetcode_session = config["leetcode_session"]
    csrf_token = config["leetcode_csrf_token"]

    configuration = lc.Configuration()

    configuration.api_key["x-csrftoken"] = csrf_token
    configuration.api_key["csrftoken"] = csrf_token
    configuration.api_key["LEETCODE_SESSION"] = leetcode_session
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    return lc.DefaultApi(lc.ApiClient(configuration))


def get_question_detail(api_instance: lc.DefaultApi, title_slug: str) -> str:
    graphql_request = lc.GraphqlQuery(
        query="""
            query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                boundTopicId
                title
                content
                translatedTitle
                isPaidOnly
                difficulty
                status
                sampleTestCase
            }
            }
        """,
        variables=lc.GraphqlQueryGetQuestionDetailVariables(title_slug=title_slug),
        operation_name="getQuestionDetail",
    )

    res = api_instance.graphql_post(body=graphql_request)

    return res.data.question.content


def get_question_by_id(api_instance: lc.DefaultApi, question_id: int) -> str:
    graphql_request = lc.GraphqlQuery(
        query="""
            query getQuestionDetail($questionId: String!) {
            question(questionId: $questionId) {
                questionId
                questionFrontendId
                boundTopicId
                title
                content
                translatedTitle
                isPaidOnly
                difficulty
                status
                sampleTestCase
            }
            }
        """,
        variables=lc.GraphqlQueryGetQuestionDetailVariables(question_id=question_id),
        operation_name="getQuestionDetail",
    )

    res = api_instance.graphql_post(body=graphql_request)

    return res.data.question.content

def display_question_content(content: str):    
    print(ht.html2text(content))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", type=str)     
    args = parser.parse_args()
    
    api_instance = get_instance()
    
    try:
        question_id = int(args.question)
        method = get_question_by_id
    except ValueError:
        method = get_question_detail
        
    content = method(api_instance, args.question)
    display_question_content(content)
    