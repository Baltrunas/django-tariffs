# django-tariffs


	def public_tariffs(self):
		return self.tariffs.filter(public=True)

	def public_tariffs_options(self):
		options = []
		for tariff in self.public_tariffs():
			for option in tariff.options_list():
				options.append(option)
		return set(options)

	def public_tariffs_properties(self):
		properties = []
		for tariff in self.public_tariffs():
			for propert in tariff.property_list():
				properties.append(propert)
		return set(properties)
