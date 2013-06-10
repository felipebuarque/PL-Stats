package in980.rgms.presentation.actions;

import in980.rgms.domain.DissertacaoMestrado;
import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.domain.Publicacao;
import in980.rgms.persistence.LinhaPesquisaDAO;
import in980.rgms.persistence.MembroDAO;

import java.util.ArrayList;
import java.util.List;

import com.opensymphony.xwork2.ActionContext;

public abstract class ActionPublicacaoBase implements ActionCRUDBase{
	private Publicacao publicacao;
	
	public List<Membro> getMembros(){
		return new MembroDAO().listaTodos();
	}
	public List<LinhaPesquisa> getLinhasPesquisa(){
		return new LinhaPesquisaDAO().listaTodos();
	}
	
	//#ifdef informacoesContextuais
	protected void loadContextualInfo(Publicacao dissertacaoMestrado) {
		Membro membroAutenticado = getMembroAutenticado();
		if(membroAutenticado != null){
			List<Membro> autores = new ArrayList<Membro>();
			autores.add(membroAutenticado);
			dissertacaoMestrado.setAutoresMembros(autores);
			
			List<LinhaPesquisa> linhaDePesquisa = membroAutenticado.getLinhasPesquisa();
			dissertacaoMestrado.setLinhasPesquisa(linhaDePesquisa);			
		}
	}
	//#endif
	
	//#ifdef autenticacao
	protected Membro getMembroAutenticado() {
		return (Membro)ActionContext.getContext().getSession().get("membroAutenticado");		
	}
	//#endif
	
	public Publicacao getPublicacao() {
		return publicacao;
	}

	public void setPublicacao(Publicacao publicacao) {
		this.publicacao = publicacao;
	}
}
