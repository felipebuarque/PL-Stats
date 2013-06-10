package in980.rgms.presentation.actions;

import in980.rgms.domain.Membro;
import in980.rgms.domain.Usuario;
import in980.rgms.persistence.MembroDAO;
import in980.rgms.persistence.UsuarioDAO;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Result;

import com.opensymphony.xwork2.ActionContext;

public class AutenticacaoAction {
	
	private Usuario usuario;
	private String msg;
	

	@Action(value = "autentica", results = { 
			@Result(name="valido", location="/index.jsp"),
		    @Result(name="invalido", location="/login.jsp") 
			}
	)
	public String login() {
		try {
			usuario = new UsuarioDAO().checaLogin(usuario);
			if (usuario != null) {
			    ActionContext.getContext().getSession().put("usuarioAutenticado", usuario);
			    Membro membro = new Membro(); 
			    membro.setUsuario(usuario);
			    membro = new MembroDAO().buscaPeloUsuario(usuario);
			    if(membro != null){
			    	ActionContext.getContext().getSession().put("membroAutenticado", membro);
			    }
			    return "valido";
			}
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("Erro ao Logar o usuario: " +e.getMessage());
		}
		return "invalido";
		
	}
	
	public Usuario getUsuario() {
		return usuario;
	}
	
	public void setUsuario(Usuario usuario) {
		this.usuario = usuario;
	}
	

	
	public String getMsg() {
		return msg;
	}
	
	public void setMsg(String msg) {
		this.msg = msg;
	}

}
