from django.conf import settings


class Placeholders(object):
    apt = '{ServiceSiteApt}'
    cust_apt = '{MailingSiteApt}'
    cust_address1 = '{CustomerName2}'
    letter_date = '{LetterDate}'
    site_address = '{ServiceAddress}'
    site_street_number = '{ServiceStreetNumber}'
    site_city = '{ServiceCity}'
    site_state = '{ServiceState}'
    cust_name = '{CustomerName}'
    cust_address = '{MailingAddress}'
    cust_city = '{MailingCity}'
    cust_state = '{MailingState}'
    cust_zip = '{MailingZip}'
    account_number = '{AccountNumber}'
    assembly_type_present = '{AssemblyTypePresent}'
    assembly_type_required = '{AssemblyTypeRequired}'
    due_date = '{DueDate}'
    consultant_name = '{ConsultantName}'
    consultant_phone = '{ConsultantPhone}'
    plumber_packet_location = '{PlumberPacketLocation}'
    plumber_packet_address = '{PlumberPacketAddress}'
    pws_logo = '{PWSLogo}'
    pws_name = '{PWSName}'
    pws_fax = '{PWSFax}'
    pws_phone = '{PWSPhone}'
    pws_email = '{PWSEmail}'
    pws_city = '{PWSCity}'
    pws_zip = '{PWSZip}'
    pws_state = '{PWSState}'
    pws_office_address = '{PWSOfficeAddress}'
    bailee_name = '{PersonInChargeName}'
    bailee_job_title = '{PersonInChargeJobTitle}'
    left_header_block = '{LeftHeaderBlock}'
    right_header_block = '{RightHeaderBlock}'


class EMPTY_VALUE:
    pass


PWS_LOGO_TEMPLATE = '<p style="text-align: center; height: 300px;"><img src="%s%s" style="width: auto; max-height: 100%%; max-width: 100%%"></p>'


class LetterRenderer(object):
    @staticmethod
    def render(letter):
        site = letter.site
        pws = site.pws
        hazard = letter.hazard
        warnings = []
        template = letter.letter_type.template

        template = template.replace(Placeholders.left_header_block, pws.letter_left_header_block)
        template = template.replace(Placeholders.right_header_block, pws.letter_right_header_block)

        if pws.logo:
            pws_logo_replacement = PWS_LOGO_TEMPLATE % (settings.HOST, pws.logo.url)
        else:
            pws_logo_replacement = EMPTY_VALUE

        replacements = {
            Placeholders.letter_date: letter.date.strftime("%B %d, %Y"),
            Placeholders.site_address: site.address1,
            Placeholders.apt: site.apt,
            Placeholders.cust_apt: site.cust_apt,
            Placeholders.cust_address1: site.cust_address1,
            Placeholders.site_street_number: site.street_number,
            Placeholders.site_city: site.city,
            Placeholders.site_state: site.state,
            Placeholders.cust_name: site.cust_name,
            Placeholders.cust_address: site.cust_address2,
            Placeholders.cust_city: site.cust_city,
            Placeholders.cust_state: site.cust_state,
            Placeholders.cust_zip: site.cust_zip,
            Placeholders.account_number: site.cust_number,
            Placeholders.pws_name: pws.name,
            Placeholders.pws_logo: pws_logo_replacement,
            Placeholders.pws_office_address: pws.office_address,
            Placeholders.pws_city: pws.city,
            Placeholders.pws_state: pws.state,
            Placeholders.pws_phone: pws.phone,
            Placeholders.pws_fax: pws.fax,
            Placeholders.pws_email: pws.email,
            Placeholders.pws_zip: pws.zip,
            Placeholders.consultant_name: pws.consultant_name,
            Placeholders.consultant_phone: pws.consultant_phone,
            Placeholders.plumber_packet_location: pws.plumber_packet_location,
            Placeholders.plumber_packet_address: pws.plumber_packet_address,
            Placeholders.bailee_name: pws.bailee_name,
            Placeholders.bailee_job_title: pws.bailee_job_title,
        }
        if hazard:
            if hazard.bp_device:
                replacements[Placeholders.assembly_type_present] = hazard.bp_device.bp_type_present
            else:
                warnings.append(Placeholders.assembly_type_present)
                replacements[Placeholders.assembly_type_present] = ''
            replacements[Placeholders.assembly_type_required] = hazard.bp_type_required
        else:
            warnings.append(Placeholders.assembly_type_present)
            warnings.append(Placeholders.assembly_type_required)
        replacements[Placeholders.due_date] = site.due_install_test_date.strftime("%m/%d/%Y") if site.due_install_test_date else ''
        for key, value in replacements.items():
            if not value:
                warnings.append(key)
                template = template.replace(key, u'')
            elif value is EMPTY_VALUE:
                template = template.replace(key, u'')
            else:
                template = template.replace(key, unicode(value))
        letter.rendered_body = template
        letter.save()
        return warnings
