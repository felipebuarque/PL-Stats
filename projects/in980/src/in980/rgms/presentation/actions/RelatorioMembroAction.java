package in980.rgms.presentation.actions;

import java.util.List;

import in980.rgms.domain.Membro;
import in980.rgms.domain.TipoMembro;
import in980.rgms.persistence.MembroDAO;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Result;

public class RelatorioMembroAction {
	private String msg;
	private List<Membro> membrosProfessor;
	private List<Membro> membrosEstudante;
	private List<Membro> membrosPesquisador;
	
	@Action(value = "membrosPorGrupo", results = { 
			@Result(location = "/lista_membro_grupo.jsp", name = "success") 
			}
	)
	public String membrosPorGrupo() {
		try {
			MembroDAO dao = new MembroDAO();
			membrosProfessor = dao.buscaPorTipo(TipoMembro.PROFESSOR);
			membrosEstudante = dao.buscaPorTipo(TipoMembro.ESTUDANTE);
			membrosPesquisador = dao.buscaPorTipo(TipoMembro.PESQUISADOR);
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao Listar os Membros: " + e.getMessage());
		}
				
		return "success";
	}
	
	@Action(value = "paginaPessoal", results = { 
			@Result(location = "/pagina_pessoal.jsp", name = "success") 
			}
	)
	public String paginaPessoal() {
		try {
			MembroDAO dao = new MembroDAO();
			membrosProfessor = dao.buscaPorTipo(TipoMembro.PROFESSOR);
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao Listar os Membros: " + e.getMessage());
		}
				
		return "success";
	}
	
	public List<Membro> getMembrosProfessor() {
		return membrosProfessor;
	}
	
	public void setMembrosProfessor(List<Membro> membrosProfessor) {
		this.membrosProfessor = membrosProfessor;
	}

	public List<Membro> getMembrosEstudante() {
		return membrosEstudante;
	}

	public void setMembrosEstudante(List<Membro> membrosEstudante) {
		this.membrosEstudante = membrosEstudante;
	}

	public List<Membro> getMembrosPesquisador() {
		return membrosPesquisador;
	}

	public void setMembrosPesquisador(List<Membro> membrosPesquisador) {
		this.membrosPesquisador = membrosPesquisador;
	}

	public String getMsg() {
		return msg;
	}
	
	public void setMsg(String msg) {
		this.msg = msg;
	}
}
