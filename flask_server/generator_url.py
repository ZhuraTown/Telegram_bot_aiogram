from decouple import config
from urllib.parse import quote


class GeneratorUrlFlask:

    @staticmethod
    def get_url_for_create_form(company: str, work: str, gp_id: str or int,
                                contractor: str, is_gp: bool, comp_id: int) -> str:
        """
        Сгенерировать ссылку на страницу создания формы
        Company: компания, work: наименования работ
        """
        company, work, contractor = company, work, contractor
        gp_id = str(gp_id)
        is_gp = str(int(is_gp))
        comp_id = str(comp_id)
        return f"{config('URL_SERVER')}create_form?&company={quote(company)}" \
               f"&work={quote(work)}&cont_id={gp_id}&cont={quote(contractor)}&is_gp={is_gp}&comp_id={comp_id}"

    @staticmethod
    def get_url_for_edit_form(company: str, work: str, ids: list, contractor: str,
                              gp_id: str or int, is_gp: bool, comp_id: int) -> str:
        """
        Генерация ссылки на изменение ранее созданной формы. Company: имя компании, work: наименование работ,
        ids: ID Записей из БД для изменений, contractor: Имя ГП, id_user: ID пользователя,
        is_gp: ГП отправляет запрос, comp_id: ID компании
        """
        # company_list, work_list, contractor_list = company.split(), work.split(), contractor.split()
        # company, work, contractor = '%20'.join(company_list), '%20'.join(work_list), '%20'.join(contractor_list)
        company, work, contractor = company, work, contractor
        ids = ','.join([str(i) for i in ids])
        gp_id = str(gp_id)
        is_gp = str(int(is_gp))
        comp_id = str(comp_id)
        return f"{config('URL_SERVER')}edit_form?&company={quote(company)}&cont={quote(contractor)}" \
               f"&work={quote(work)}&ids={ids}&cont_id={gp_id}&is_gp={is_gp}&comp_id={comp_id}"
