package in980.rgms.persistence;

import in980.rgms.domain.Usuario;
import in980.rgms.utils.HibernateUtils;

import java.util.List;

import org.hibernate.Session;

public class UsuarioDAO extends Dao<Usuario> {

	@SuppressWarnings("unchecked")
	protected List<Usuario> montaLista(Usuario object, Session s) {
		List<Usuario> listaRetorno = s
				.createQuery(
						"from " + getTabela()
								+ " t where upper(t.login) like :login ")
				.setString("login", "%" + object.getLogin().toUpperCase() + "%")
				.list();
		return listaRetorno;
	}

	@Override
	protected String getTabela() {
		return "Usuario";
	}

	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {
		return Usuario.class;
	}

	@SuppressWarnings("unchecked")
	public Usuario checaLogin(Usuario usuario) {
		Session s = HibernateUtils.getSessionFactory().getCurrentSession();
		List<Usuario> listaRetorno = s
				.createQuery(
						"from " + getTabela()
								+ " t where upper(t.login) like :login and " +
										" t.senha like :senha")
				.setString("login", "%" + usuario.getLogin().toUpperCase() + "%")
				.setString("senha", "%" + usuario.getSenha() + "%")
				.list();
		return listaRetorno.get(0);
	}

}
