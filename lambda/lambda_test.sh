#!/bin/bash
#emulambda -v lambda_face_analysis.lambda_handler s3put_event.json
emulambda -v lambda_normalize.lambda_handler face_analysis_event.json
