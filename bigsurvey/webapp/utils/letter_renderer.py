from django.conf import settings


class Placeholders(object):
    letter_date = '{LetterDate}'
    site_address = '{ServiceAddress}'
    site_street_number = '{ServiceStreetNumber}'
    site_city = '{ServiceCity}'
    site_state = '{ServiceState}'
    cust_name = '{CustomerName}'
    cust_address = '{CustomerAddress}'
    cust_city = '{CustomerCity}'
    cust_state = '{CustomerState}'
    cust_zip = '{CustomerZip}'
    account_number = '{AccountNumber}'
    assembly_type = '{AssemblyType}'
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
    bailee_name = '{BaileeName}'
    bailee_job_title = '{BaileeJobTitle}'
    left_header_block = '{LeftHeaderBlock}'
    right_header_block = '{RightHeaderBlock}'


class EMPTY_VALUE:
    pass


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
            pws_logo_replacement = '<p style="text-align: center; height: 250px;"><img src="%s" style="width: auto; max-height: 100%%"></p>' % pws.logo.url
        else:
            pws_logo_replacement = EMPTY_VALUE

        replacements = {
            Placeholders.letter_date: letter.date.strftime("%B %d, %Y"),
            Placeholders.site_address: site.address1,
            Placeholders.site_street_number: site.street_number,
            Placeholders.site_city: site.city,
            Placeholders.site_state: site.state,
            Placeholders.cust_name: site.cust_name,
            Placeholders.cust_address: site.cust_address1,
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
            replacements[Placeholders.assembly_type] = hazard.bp_type_required
            replacements[Placeholders.due_date] = hazard.due_install_test_date.strftime("%m/%d/%Y") if hazard.due_install_test_date else ''
        else:
            warnings.append("Warning: Letter has no Hazard specified. Was it imported?")
        for key, value in replacements.items():
            if value is None or value == '':
                warnings.append("Warning: %s has no value in database" % key)
            elif value is EMPTY_VALUE:
                template = template.replace(key, u'')
            else:
                template = template.replace(key, unicode(value))
        letter.rendered_body = template
        letter.save()
        return warnings