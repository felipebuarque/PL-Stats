package in980.rgms.presentation.actions;

import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.persistence.ArtigoConferenciaDAO;
import in980.rgms.persistence.LinhaPesquisaDAO;
import in980.rgms.persistence.MembroDAO;

import java.util.List;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.InterceptorRef;
import org.apache.struts2.convention.annotation.ParentPackage;
import org.apache.struts2.convention.annotation.Result;

@ParentPackage("default")
public class MembroAction implements ActionCRUDBase {
	
	private Membro membro;
	private List<Membro> membros;
	
	private String msg;

	@Override
	@Action(value = "excluirMembro", results = { 
			@Result(name = "success", type="redirectAction", params= {"actionName", "listarTodosMembros"}) 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String delete() {
		try {
			new MembroDAO().excluir(membro);
			setMsg("Membro : " + membro.getNome() + " excluido com sucesso.");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao excluir o membro: " +e.getMessage());
		}
		return "success";
		
	}

	@Override
	@Action(value = "inserirMembro", results = { 
			@Result(location = "/cadastro_membro.jsp", name = "success") 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String insert() {
		try {
			membro.validateToPersist();
			if(membro != null && membro.getID() !=null){
				new MembroDAO().atualizar(membro);
			} else {
				new MembroDAO().inserir(membro);
			}
			setMsg("Membro Inserido Com Sucesso");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao Cadastrar o Membro: " + e.getMessage());
		}		
		return "success";
	}
	
	@Action(value = "buscarMembros", results = { 
			@Result(location = "/lista_membro.jsp", name = "success") 
			}	
	)
	public String searchByName() {
		try {
			membros = new MembroDAO().buscar(membro);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return "success";
	}
	
	
	@Override
	@Action(value = "listarTodosMembros", results = { 
			@Result(location = "/lista_membro.jsp", name = "success") 
			}	
	)
	public String listAll() {
		membros = new MembroDAO().listaTodos();
		return "success";
	}
	
	public String update() {
		return null;
	}

	@Action(value = "mostrarMembro", results = { 
			@Result(location = "/cadastro_membro.jsp", name = "success") 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String mostrarMembro() {
		try {
			if(membro != null && membro.getID() != null){
				membro = new MembroDAO().buscaPeloId(membro.getID());
			}
						
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Membro solicitado nao existe: ");
		}
		return "success";
	}
	
	
	@Action(value = "paginaMembro", results = { 
			@Result(location = "/rel_pessoal_membro.jsp", name = "success") 
			}
	)
	public String paginaMembro() {
		try {
			membro = new MembroDAO().buscaPeloId(membro.getID());
			
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Membro solicitado nao existe: ");
		}
		return "success";
	}
	
	
	public Membro getMembro() {
		return membro;
	}
	public void setMembro(Membro membro) {
		this.membro = membro;
	}
	public List<Membro> getMembros() {
		return membros;
	}
	public void setMembros(List<Membro> membros) {
		this.membros = membros;
	}
	public String getMsg() {
		return msg;
	}
	public void setMsg(String msg) {
		this.msg = msg;
	}

	public List<LinhaPesquisa> getLinhasPesquisa(){
		return new LinhaPesquisaDAO().listaTodos();
	}	

}
