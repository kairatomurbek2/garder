from webapp import models
from random import randint

ALPHAS = ['A', 'B', 'C', 'D', 'E']
TF = [True, False]


class Generator(object):
    def generate(self):
        self.generate_customers()
        self.generate_pws()
        self.generate_sites()

    def generate_customers(self):
        i = 0
        for s in ALPHAS:
            for ss in ALPHAS:
                for sss in ALPHAS:
                    i += 1
                    number = "%s%s%s" % (s, ss, sss)
                    name = "Name%s Surname%s, son of Father%s " % (s, ss, sss)
                    city = "City of %s%s%s" % (sss, ss, s)
                    address = "%s%s Street, %s" % (s, ss, sss)
                    zzip = "{:0>5d}".format(i)
                    code = models.CustomerCode.objects.get(pk=randint(1, 10))
                    state = models.STATES[randint(0, 50)][0]
                    models.Customer.objects.create(
                        number=number,
                        name=name,
                        code=code,
                        address1=address,
                        city=city,
                        state=state,
                        zip=zzip
                    )

    def generate_pws(self):
        i = 0
        for s in ALPHAS:
            i += 1
            number = "%s%s%s" % (s, s, i)
            name = "PWS%s" % s
            models.PWS.objects.create(
                number=number,
                name=name
            )

    def generate_sites(self):
        random_probs = [2, 2, 2, 2, 2, 2, 3, 3, 3, 4]
        j = 0
        for customer in models.Customer.objects.all():
            pws = models.PWS.objects.get(pk=randint(3, 7))
            for i in range(1, random_probs[randint(0, 9)]):
                j += 1
                status = models.SiteStatus.objects.get(pk=randint(1, 3))
                address = "%s%s Street, %s" % (
                    ALPHAS[randint(0, 4)],
                    ALPHAS[randint(0, 4)],
                    ALPHAS[randint(0, 4)]
                )
                city = customer.city
                state = models.STATES[randint(0, 50)][0]
                zzip = "{:0>5d}".format(j)
                site_use = models.SiteUse.objects.get(pk=randint(1, 8))
                site_type = models.SiteType.objects.get(pk=randint(1, 85))
                potable = TF[randint(0, 1)]
                fire = TF[randint(0, 1)]
                irrigation = TF[randint(0, 1)]
                is_due_install = TF[randint(0, 1)]
                is_backflow_present = TF[randint(0, 1)]
                models.Site.objects.create(
                    status=status,
                    customer=customer,
                    pws=pws,
                    address1=address,
                    city=city,
                    state=state,
                    zip=zzip,
                    site_use=site_use,
                    site_type=site_type,
                    potable_present=potable,
                    fire_present=fire,
                    irrigation_present=irrigation,
                    is_due_install=is_due_install,
                    is_backflow=is_backflow_present
                )