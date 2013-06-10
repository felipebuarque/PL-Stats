package in980.rgms.presentation.actions;

import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.domain.Publicacao;
import in980.rgms.persistence.LinhaPesquisaDAO;
import in980.rgms.persistence.MembroDAO;
import in980.rgms.persistence.PublicacaoDAO;

import java.util.List;
import java.util.Set;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Result;

public class LinhaPesquisaAction implements ActionCRUDBase {

	private LinhaPesquisa linhaPesquisa;
	private List<LinhaPesquisa> linhasPesquisa;

	private String msg;

	@Override
	@Action(value = "excluirLinhaPesquisa", results = { @Result(name = "success", type = "redirectAction", params = {
			"actionName", "listarTodasLinhasPesquisa" }) })
	public String delete() {
		try {
			new LinhaPesquisaDAO().excluir(linhaPesquisa);
			setMsg("Membro : " + linhaPesquisa.getDescricao()
					+ " excluido com sucesso.");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao excluir a Linha de Pesquisa: " + e.getMessage());
		}
		return "success";

	}

	@Override
	@Action(value = "inserirLinhaPesquisa", results = { @Result(location = "/cadastro_linha_pesquisa.jsp", name = "success") })
	public String insert() {
		try {
			linhaPesquisa.validateToPersist();
			if (linhaPesquisa != null && linhaPesquisa.getID() != null) {
				new LinhaPesquisaDAO().atualizar(linhaPesquisa);
			} else {
				new LinhaPesquisaDAO().inserir(linhaPesquisa);
			}
			setMsg("Linha de Pesquisa Inserida Com Sucesso");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao Cadastrar a Linha de Pesquisa: " + e.getMessage());
		}
		return "success";
	}

	@Action(value = "buscarLinhasPesquisa", results = { @Result(location = "/lista_linhas_pesquisas.jsp", name = "success") })
	public String searchByDescription() {
		try {
			linhasPesquisa = new LinhaPesquisaDAO().buscar(linhaPesquisa);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return "success";
	}

	@Override
	@Action(value = "listarTodasLinhasPesquisa", results = { @Result(location = "/lista_linha_pesquisa.jsp", name = "success") })
	public String listAll() {
		linhasPesquisa = new LinhaPesquisaDAO().listaTodos();
		return "success";
	}

	public String update() {
		return null;
	}

	@Action(value = "mostrarLinhaPesquisa", results = { @Result(location = "/cadastro_linha_pesquisa.jsp", name = "success") })
	public String mostrarLinhaPesquisa() {
		try {
			if (linhaPesquisa != null && linhaPesquisa.getID() != null) {
				linhaPesquisa = new LinhaPesquisaDAO()
						.buscaPeloId(linhaPesquisa.getID());
			}
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Linha de Pesquisa solicitada nao existe: ");
		}
		return "success";
	}

	public LinhaPesquisa getLinhaPesquisa() {
		return linhaPesquisa;
	}

	public void setLinhaPesquisa(LinhaPesquisa linhaPesquisa) {
		this.linhaPesquisa = linhaPesquisa;
	}

	public List<LinhaPesquisa> getLinhasPesquisa() {
		return linhasPesquisa;
	}

	public void setLinhasPesquisa(List<LinhaPesquisa> linhasPesquisas) {
		this.linhasPesquisa = linhasPesquisas;
	}

	public String getMsg() {
		return msg;
	}

	public void setMsg(String msg) {
		this.msg = msg;
	}

	public List<Membro> getMembros() {
		List<Membro> listMembros = new MembroDAO().listaTodos();
		return listMembros;
	}

	public List<Publicacao> getPublicacoes() {
		return new PublicacaoDAO().listaTodos();
	}
}
