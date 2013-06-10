package in980.rgms.domain.aspect;

import in980.rgms.domain.Usuario;
import in980.rgms.domain.Membro;

import javax.persistence.CascadeType;
import javax.persistence.FetchType;
import javax.persistence.OneToOne;


public aspect Autenticacao {
//inter-type declaration
	//pointcut addUsuario() :
	
	@OneToOne(cascade={CascadeType.ALL}, fetch = FetchType.LAZY)
	private Usuario Membro.usuario;
	public Usuario Membro.getUsuario() {
		return usuario;
	}
	public void Membro.setUsuario(Usuario usuario) {
		this.usuario = usuario;
	}	
}
