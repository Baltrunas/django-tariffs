
class TariffAddition(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=256)
	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	price = models.PositiveIntegerField(verbose_name=_('Price'), default=1000, null=True, blank=True)

	price_from = models.BooleanField(verbose_name=_('Price From'), default=False)
	price_after = models.CharField(verbose_name=_('Price After'), max_length=256, blank=True, null=True)

	selected = models.BooleanField(verbose_name=_('Selected'), default=True)
	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['order']
		verbose_name = _('Tariff Addition')
		verbose_name_plural = _('Tariffs Additions')


class Tariff(models.Model):
	block = models.ForeignKey(Block, verbose_name=_('Block'), related_name='tariffs')

	title = models.CharField(verbose_name=_('Title'), max_length=256)
	sub_title = models.CharField(verbose_name=_('Sub Title'), max_length=256)

	old_price = models.PositiveIntegerField(verbose_name=_('Old Price'), default=1000, null=True, blank=True)
	new_price = models.PositiveIntegerField(verbose_name=_('New Price'), default=1000, null=True, blank=True)

	price_from = models.BooleanField(verbose_name=_('Price From'), default=False)
	price_after = models.CharField(verbose_name=_('Price After'), max_length=256, blank=True, null=True)

	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	options = models.TextField(verbose_name=_('Options'), blank=True, null=True)

	image = models.FileField(verbose_name=_('Image'), upload_to='tariff/image', blank=True, null=True)

	order_url = models.URLField(verbose_name=_('Order URL'), max_length=256, blank=True, null=True)

	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	additions = models.ManyToManyField(TariffAddition, verbose_name=_('Additions'), blank=True, related_name='tariff')

	vip = models.BooleanField(verbose_name=_('VIP'), default=True)
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def options_list(self):
		options_list = []
		for option in self.options.split("\n"):
			if len(option.split(": ")) < 2:
				options_list.append(option.strip())
		return options_list

	def property_list(self):
		property_list = []
		for option in self.options.split("\n"):
			property_value = option.split(": ")
			if len(property_value) > 1:
				property_list.append(property_value[0].strip())
		return property_list

	def get_property_value(self, propert):
		for option in self.options.split("\n"):
			property_value = option.split(": ")
			if len(property_value) > 1:
				if property_value[0].strip() == propert:
					return property_value[1].strip()

	def public_additions(self):
		return self.additions.filter(public=True)

	@models.permalink
	def url(self):
		return ('tariff', (), {'id': self.id})

	def get_absolute_url(self):
		if self.order_url:
			return self.order_url
		else:
			return self.url()

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['order']
		verbose_name = _('Tariff')
		verbose_name_plural = _('Tariffs')


class TariffOrder(models.Model):
	site = models.ForeignKey(Site, verbose_name=_('Site'), blank=True, null=True)

	name = models.CharField(max_length=128, verbose_name=_('Name'), help_text=_('Gleb'))
	phone = models.CharField(max_length=32, verbose_name=_('Phone'), help_text=_('+7 (965) 222-03-30'))
	email = models.EmailField(max_length=128, verbose_name=_('E-Mail'), help_text=_('gleb@gmail.com'))

	ip = models.GenericIPAddressField(blank=True, null=True, editable=False, verbose_name=_('IP'))
	referrer = models.CharField(verbose_name=_('Referrer'), max_length=2048, blank=True, null=True, editable=False)

	tariff = models.ForeignKey(Tariff, verbose_name=_('Tariff'), null=True)
	additions = models.ManyToManyField(TariffAddition, verbose_name=_('Additions'), blank=True)

	total_price = models.PositiveIntegerField(verbose_name=_('Total Price'), null=True, blank=True)

	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return '#%s from %s' % (self.pk, self.name)

	class Meta:
		ordering = ['-created_at']
		verbose_name = _('Tariff Order')
		verbose_name_plural = _('Tariff Orders')
