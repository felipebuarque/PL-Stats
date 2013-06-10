package in980.rgms.presentation.actions;

import in980.rgms.domain.ArtigoConferencia;
import in980.rgms.domain.ArtigoRevista;
import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.domain.Publicacao;
import in980.rgms.persistence.ArtigoRevistaDAO;
import in980.rgms.persistence.LinhaPesquisaDAO;
import in980.rgms.persistence.MembroDAO;

import java.util.List;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.InterceptorRef;
import org.apache.struts2.convention.annotation.InterceptorRefs;
import org.apache.struts2.convention.annotation.ParentPackage;
import org.apache.struts2.convention.annotation.Result;

@ParentPackage("default")
public class ArtigoRevistaAction extends ActionPublicacaoBase {
	
	private Publicacao publicacao;
	private ArtigoRevista artigoRevista;

	private String msg;

	@Override
	@Action(value = "excluirartigoRevista", results = { 
			@Result(name = "success", 
					type="redirectAction", 
					params= {"actionName", "listarTodasPublicacoes"}) 
			}
	//#ifdef autenticacao
	, interceptorRefs = { @InterceptorRef("autenticacao")} 
	//#endif 
	)
	public String delete() {
		try {
			new ArtigoRevistaDAO().excluir(artigoRevista);
			
		} catch (Exception e) {
			e.printStackTrace();
			
		}
		return "success";
	}

	@Override
	@Action(value = "inserirArtigoRevista", results = { 
			@Result(location = "/cadastra_artigo_revista.jsp", 
					name = "success") 
			}
			//#ifdef autenticacao
			, interceptorRefs = { @InterceptorRef("autenticacao"), @InterceptorRef("defaultStack")} 
			//#endif 
	)
	public String insert() {
		try {
			artigoRevista.validateToPersist();
			if(artigoRevista.getID() == null){
				new ArtigoRevistaDAO().inserir(artigoRevista);
			}else{
				new ArtigoRevistaDAO().atualizar(artigoRevista);
			}
			setMsg("Artigo inserido com sucesso");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao inser o Artigo:"  + e.getMessage());
		}
		return "success";
	}

	@Override
	public String listAll() {
		return null;
	}
	
	@Action(value = "mostrarartigoRevista", results = { 
			@Result(location = "/cadastra_artigo_revista.jsp", name = "success") 
		}
	//#ifdef autenticacao
	, interceptorRefs = { @InterceptorRef("autenticacao")} 
	//#endif 
	)
	public String mostrarArtigoRevista(){
		try {
			if(artigoRevista != null && artigoRevista.getID() != null){
				artigoRevista = new ArtigoRevistaDAO().buscaPeloId(artigoRevista.getID());
			}
			//#ifdef informacoesContextuais
			else{
				artigoRevista = new ArtigoRevista();
				super.loadContextualInfo(artigoRevista);
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

	public ArtigoRevista getArtigoRevista() {
		return artigoRevista;
	}

	public void setArtigoRevista(ArtigoRevista artigoRevista) {
		this.artigoRevista = artigoRevista;
	}
	
}
