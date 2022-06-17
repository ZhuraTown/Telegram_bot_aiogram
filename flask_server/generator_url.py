from decouple import config

class GeneratorUrlFlask:

    @staticmethod
    def get_url_for_create_form(company: str, work: str) -> str:
        """
        Company: компания, work: наименования работ
        """
        company_list, work_list = company.split(), work.split()
        company, work = '%20'.join(company_list), '%20'.join(work_list)

        return f"{config('URL_SERVER')}create_form?&company={company}&work={work}"

    @staticmethod
    def get_url_for_edit_form(company: str, work: str, ids: list, contractor: str) -> str:
        company_list, work_list, contractor_list = company.split(), work.split(), contractor.split()
        company, work, contractor = '%20'.join(company_list), '%20'.join(work_list), '%20'.join(contractor_list)
        ids = ','.join([str(i) for i in ids])
        return f"{config('URL_SERVER')}see_form?&company={company}&contractor={contractor}&work={work}&ids={ids}"
