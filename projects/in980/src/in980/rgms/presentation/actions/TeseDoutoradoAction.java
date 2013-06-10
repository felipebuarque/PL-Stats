package in980.rgms.presentation.actions;

import in980.rgms.domain.DissertacaoMestrado;
import in980.rgms.domain.Publicacao;
import in980.rgms.domain.TeseDoutorado;
import in980.rgms.persistence.TeseDoutoradoDAO;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.InterceptorRef;
import org.apache.struts2.convention.annotation.ParentPackage;
import org.apache.struts2.convention.annotation.Result;

@ParentPackage("default")
public class TeseDoutoradoAction extends ActionPublicacaoBase {
	
	private Publicacao publicacao;
	private TeseDoutorado teseDoutorado;

	private String msg;

	@Override
	@Action(value = "excluirteseDoutorado", results = { 
			@Result(name = "success", 
					type="redirectAction", 
					params= {"actionName", "listarTodasPublicacoes"}) 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String delete() {
		try {
			new TeseDoutoradoDAO().excluir(teseDoutorado);
			
		} catch (Exception e) {
			e.printStackTrace();
			
		}
		return "success";
	}

	@Override
	@Action(value = "inserirTeseDoutorado", results = { 
			@Result(location = "/cadastra_tese_doutorado.jsp", 
					name = "success") 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String insert() {
		try {
			teseDoutorado.validateToPersist();
			if(teseDoutorado.getID() == null){
				new TeseDoutoradoDAO().inserir(teseDoutorado);
			}else{
				new TeseDoutoradoDAO().atualizar(teseDoutorado);
			}
			setMsg("Tese inserido com sucesso");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao inserir a Tese:"  + e.getMessage());
		}
		return "success";
	}

	@Override
	public String listAll() {
		return null;
	}
	
	@Action(value = "mostrarteseDoutorado", results = { 
			@Result(location = "/cadastra_tese_doutorado.jsp", name = "success") 
		}
		//#ifdef autenticacao
		, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
		//#endif 
	)
	public String mostrarTeseDoutorado(){
		try {
			if(teseDoutorado != null && teseDoutorado.getID() != null){
				teseDoutorado = new TeseDoutoradoDAO().buscaPeloId(teseDoutorado.getID());
			}
			//#ifdef informacoesContextuais
			else{
				teseDoutorado = new TeseDoutorado();
				super.loadContextualInfo(teseDoutorado);
				teseDoutorado.setEscola(getMembroAutenticado().getUniversidade());
			}
			//#endif 
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Artigo solicitado nao existe: ");
		}
		return "success";
	}

	@Override
	public String update() {
		return null;
	}

	public Publicacao getPublicacao() {
		return publicacao;
	}

	public void setPublicacao(Publicacao publicacao) {
		this.publicacao = publicacao;
	}

	public String getMsg() {
		return msg;
	}

	public void setMsg(String msg) {
		this.msg = msg;
	}

		public TeseDoutorado getTeseDoutorado() {
		return teseDoutorado;
	}

	public void setTeseDoutorado(TeseDoutorado teseDoutorado) {
		this.teseDoutorado = teseDoutorado;
	}
	
}
