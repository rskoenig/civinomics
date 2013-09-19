


class HomezController(BaseController):

	def index(self):

		if 'user' in session:
			# check to see if County and City have same name
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
            # fetching geos and mapping them to local variables
            c.scopeMapping = [    ('earth', 'Earth'),
                            ('country', c.authuser_geo['countryTitle']),
                            ('state', c.authuser_geo['stateTitle']),
                            ('county', county),
                            ('city', city),
                            ('postalCode', c.authuser_geo['postalCode'])
                            ]

