package in980.rgms.presentation.actions;

import in980.rgms.domain.ArtigoConferencia;
import in980.rgms.domain.ArtigoRevista;
import in980.rgms.domain.DissertacaoMestrado;
import in980.rgms.domain.Publicacao;
import in980.rgms.domain.TeseDoutorado;
import in980.rgms.persistence.ArtigoConferenciaDAO;
import in980.rgms.persistence.ArtigoRevistaDAO;
import in980.rgms.persistence.DissertacaoMestradoDAO;
import in980.rgms.persistence.PublicacaoDAO;
import in980.rgms.persistence.TeseDoutoradoDAO;

import java.util.List;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Result;

public class ListarPublicacaoAction {
	
	private List publicacoes;
	private String tituloPublicacao;
	private Integer ano;
	
	@Action(value = "mudaLocaleLingua", results = { 
			@Result(location = "/index.jsp", name = "success") 
			}	
	)
	public String mudaLocaleLingua() {		
		return "success";
	}
	
	@SuppressWarnings("unchecked")
	@Action(value = "listarTodasPublicacoes", results = { 
			@Result(location = "/lista_publicacao.jsp", name = "success") 
			}	
	)
	public String listAll() {
		publicacoes = new ArtigoRevistaDAO().listaTodos();
		publicacoes.addAll(new ArtigoConferenciaDAO().listaTodos());
		publicacoes.addAll(new DissertacaoMestradoDAO().listaTodos());
		publicacoes.addAll(new TeseDoutoradoDAO().listaTodos());
		return "success";
	}
	
	
	@SuppressWarnings("unchecked")
	@Action(value = "buscarPublicacoesPeloTitulo", results = { 
			@Result(location = "/lista_publicacao.jsp", name = "success") 
			}	
	)
	public String searchByName() throws Exception {
		ArtigoConferencia ac = new ArtigoConferencia();
		ac.setTitulo(tituloPublicacao);
		ac.setAno(ano);
		
		publicacoes = new PublicacaoDAO().buscar(ac);		
		return "success";
	}

	public List getPublicacoes() {
		return publicacoes;
	}
	

	public void setPublicacoes(List<? extends Publicacao> publicacoes) {
		this.publicacoes = publicacoes;
	}


	public String getTituloPublicacao() {
		return tituloPublicacao;
	}


	public void setTituloPublicacao(String tituloPublicacao) {
		this.tituloPublicacao = tituloPublicacao;
	}

	public Integer getAno() {
		return ano;
	}

	public void setAno(Integer ano) {
		this.ano = ano;
	}




}
