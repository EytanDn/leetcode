import leetcode as lc
import yaml

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

api_instance = lc.DefaultApi(lc.ApiClient(configuration))


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
    variables=lc.GraphqlQueryGetQuestionDetailVariables(title_slug="two-sum"),
    operation_name="getQuestionDetail",
)

res = api_instance.graphql_post(body=graphql_request)

print(res.data.question.content)