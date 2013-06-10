package in980.rgms.presentation.actions;

import in980.rgms.domain.ArtigoConferencia;
import in980.rgms.domain.DissertacaoMestrado;
import in980.rgms.persistence.ArtigoConferenciaDAO;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.InterceptorRef;
import org.apache.struts2.convention.annotation.ParentPackage;
import org.apache.struts2.convention.annotation.Result;

@ParentPackage("default")
public class ArtigoConferenciaAction extends ActionPublicacaoBase {

	private ArtigoConferencia artigoConferencia;

	private String msg;

	@Override
	@Action(value = "excluirartigoConferencia", results = { @Result(name = "success", type = "redirectAction", params = {
			"actionName", "listarTodasPublicacoes" }) } 
	//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
	//#endif 
	)
	public String delete() {
		try {
			new ArtigoConferenciaDAO().excluir(artigoConferencia);

		} catch (Exception e) {
			e.printStackTrace();

		}
		return "success";
	}

	@Override
	@Action(value = "inserirArtigoConferencia", results = { @Result(location = "/cadastra_artigo_conferencia.jsp", name = "success") }
	//#ifdef autenticacao
	, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
	//#endif 
	)
	public String insert() {
		try {
			artigoConferencia.validateToPersist();
			if (artigoConferencia.getID() == null) {
				new ArtigoConferenciaDAO().inserir(artigoConferencia);
			} else {
				new ArtigoConferenciaDAO().atualizar(artigoConferencia);
			}
			setMsg("Artigo inserido com sucesso");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao inserir o Artigo:" + e.getMessage());
		}
		return "success";
	}

	@Override
	public String listAll() {
		return null;
	}

	@Action(value = "mostrarartigoConferencia", results = { @Result(location = "/cadastra_artigo_conferencia.jsp", name = "success") }
	//#ifdef autenticacao
	, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
	//#endif 
	)
	public String mostrarArtigoConferencia() {
		try {
			if (artigoConferencia != null && artigoConferencia.getID() != null) {
				artigoConferencia = new ArtigoConferenciaDAO()
						.buscaPeloId(artigoConferencia.getID());
			}
			//#ifdef informacoesContextuais
			else{
				artigoConferencia = new ArtigoConferencia();
				super.loadContextualInfo(artigoConferencia);
			}
			//#endif

		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Artigo solicitado nao existe: ");
		}
		return "success";
	}

	public String update() {
		return null;
	}

	public String getMsg() {
		return msg;
	}

	public void setMsg(String msg) {
		this.msg = msg;
	}

	public ArtigoConferencia getArtigoConferencia() {
		return artigoConferencia;
	}

	public void setArtigoConferencia(ArtigoConferencia artigoConferencia) {
		this.artigoConferencia = artigoConferencia;
	}

}
