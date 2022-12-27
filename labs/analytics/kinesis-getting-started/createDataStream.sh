aws kinesis create-stream --stream-name ExampleInputStream
sleep 30
aws kinesis describe-stream-summary --stream-name ExampleInputStream