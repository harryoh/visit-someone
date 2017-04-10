#!/bin/bash
emulambda -v lambda_face_analysis.lambda_handler sample_cloudwatch_event.json
emulambda -v lambda_normalize.lambda_handler sample_face_analysis_event.json
ES_ENDPOINT='search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com' emulambda -v lambda_post_elasticsearch.lambda_handler sample_normalize.json
