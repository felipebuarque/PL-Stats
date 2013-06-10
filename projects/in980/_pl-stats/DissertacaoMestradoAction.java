package in980.rgms.presentation.actions;

import in980.rgms.domain.DissertacaoMestrado;
import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.domain.Publicacao;
import in980.rgms.persistence.DissertacaoMestradoDAO;

import java.util.ArrayList;
import java.util.List;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.InterceptorRef;
import org.apache.struts2.convention.annotation.ParentPackage;
import org.apache.struts2.convention.annotation.Result;

import com.opensymphony.xwork2.ActionContext;

@ParentPackage("default")
public class DissertacaoMestradoAction extends ActionPublicacaoBase{
	
	
	private DissertacaoMestrado dissertacaoMestrado;

	private String msg;

	@Override
	@Action(value = "excluirdissertacaoMestrado", results = { 
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
			new DissertacaoMestradoDAO().excluir(dissertacaoMestrado);
			
		} catch (Exception e) {
			e.printStackTrace();
			
		}
		return "success";
	}

	@Override
	@Action(value = "inserirDissertacaoMestrado", results = { 
			@Result(location = "/cadastra_dissertacao_mestrado.jsp", 
					name = "success") 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String insert() {
		try {
			dissertacaoMestrado.validateToPersist();
			if(dissertacaoMestrado.getID() == null){
				new DissertacaoMestradoDAO().inserir(dissertacaoMestrado);
			}else{
				new DissertacaoMestradoDAO().atualizar(dissertacaoMestrado);
			}
			setMsg("Dissertacao inserido com sucesso");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao inserir o Dissertacao:"  + e.getMessage());
		}
		return "success";
	}

	@Override
	public String listAll() {
		return null;
	}
	
	@Action(value = "mostrardissertacaoMestrado", results = { 
			@Result(location = "/cadastra_dissertacao_mestrado.jsp", name = "success") 
		}
		//#ifdef autenticacao
		, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
		//#endif 
	)
	public String mostrarDissertacaoMestrado(){
		try {
			if(dissertacaoMestrado != null && dissertacaoMestrado.getID() != null){
				dissertacaoMestrado = new DissertacaoMestradoDAO().buscaPeloId(dissertacaoMestrado.getID());
			} 
			//#ifdef informacoesContextuais
			else{
				dissertacaoMestrado = new DissertacaoMestrado();
				super.loadContextualInfo(dissertacaoMestrado);
				dissertacaoMestrado.setEscola(getMembroAutenticado().getUniversidade());
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

	

	public String getMsg() {
		return msg;
	}

	public void setMsg(String msg) {
		this.msg = msg;
	}

	public DissertacaoMestrado getDissertacaoMestrado() {
		return dissertacaoMestrado;
	}

	public void setDissertacaoMestrado(DissertacaoMestrado dissertacaoMestrado) {
		this.dissertacaoMestrado = dissertacaoMestrado;
	}
	
}
