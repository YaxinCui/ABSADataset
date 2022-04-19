	####README###
	
SemEval-2016 Task 5 - Aspect-Based Sentiment Analysis
Turkish Telecom Twitter Dataset

Please follow the steps below to fill sample data content to xml file.

	1- Generate the tokens from Twitter to use the public Twitter API. Tokens can be generated as expressed in https://dev.twitter.com/oauth/overview/application-owner-access-tokens

	2- Get Access Token, Access Token Secret, Consumer Key, Consumer Secret.

	3- Install tweepy 
		# pip install tweepy
		if you have any problems while installing please visit https://github.com/tweepy/tweepy

	4- Run command below:
		# python semeval_absa_turkish.py "ACCESS_TOKEN" "ACCESS_TOKEN_SECRET" "CONSUMER_KEY" "CONSUMER_KEY_SECRET"

	5- That's all. The unmasked file is ready to use in current directory. (telecom_trial_turkish_final_unmasked.xml)

Note: Python script file(semeval_absa_turkish.py) and data file(telecom_trial_turkish_final.xml) file should be in the same directory. Python 2.7 is required.


	
	


