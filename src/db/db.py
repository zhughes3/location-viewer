

import boto3
import decimal
from geopy.geocoders import Nominatim

tablename = 'locations'
geolocator = Nominatim()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)
for item in table.scan()['Items']:
	i_id = item['id']
	address = item['street'] + ' ' + item['city'] + ', ' + item['state']
	print(address)
	location = geolocator.geocode(address)
	if location is not None:
		print(location.latitude, location.longitude)
		response = table.update_item(
			Key={ 'id': i_id },
			UpdateExpression='set latitude=:la, longitude=:lo',
			ConditionExpression='attribute_not_exists(latitude) && attribute_not_exists(longitude)',
			ExpressionAttributeValues={
				':la': decimal.Decimal(location.latitude),
				':lo': decimal.Decimal(location.longitude)
			},
			ReturnValues='UPDATED_NEW'
		)
		
