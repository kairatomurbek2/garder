class Placeholders(object):
        letter_date = '{LetterDate}'
        site_address = '{ServiceAddress}'
        site_city = '{ServiceCity}'
        cust_name = '{CustomerName}'
        cust_address = '{CustomerAddress}'
        cust_city = '{CustomerCity}'
        cust_state = '{CustomerState}'
        cust_zip = '{CustomerZip}'
        account_number = '{AccountNumber}'
        assembly_type = '{AssemblyType}'
        contact_email = '{ContactEmail}'
        due_date = '{DueDate}'
        pp_location = '{PlumberPacketLocation}'
        pp_address = '{PlumberPacketAddress}'


class LetterRenderer(object):
    @staticmethod
    def render(letter):
        site = letter.site
        hazard = letter.hazard
        warnings = []
        replacements = {
            Placeholders.letter_date: letter.date,
            Placeholders.site_address: site.address1,
            Placeholders.site_city: site.city,
            Placeholders.cust_name: site.cust_name,
            Placeholders.cust_address: site.cust_address1,
            Placeholders.cust_city: site.cust_city,
            Placeholders.cust_state: site.cust_state,
            Placeholders.cust_zip: site.cust_zip,
            Placeholders.account_number: site.cust_number,
            Placeholders.contact_email: letter.user.email,
            Placeholders.pp_address: "Plumber Packet Address",
            Placeholders.pp_location: "Plumber Packet Location",
        }
        if hazard:
            replacements[Placeholders.assembly_type] = hazard.bp_type_required
            replacements[Placeholders.due_date] = hazard.due_install_test_date
        else:
            warnings.append("Warning: Letter has no Hazard specified. Was it imported?")
        template = letter.letter_type.template
        for key in replacements.keys():
            replacement = replacements[key]
            if replacement is None or replacement == "":
                warnings.append("Warning: %s has no value in database" % key)
            else:
                template = template.replace(key, unicode(replacement))
        letter.rendered_body = template
        letter.save()
        return warnings