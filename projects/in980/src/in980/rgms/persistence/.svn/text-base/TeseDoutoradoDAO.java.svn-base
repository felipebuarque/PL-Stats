package in980.rgms.persistence;

import in980.rgms.domain.TeseDoutorado;

import java.util.List;

import org.hibernate.Session;

public class TeseDoutoradoDAO extends Dao<TeseDoutorado>{

	@Override
	protected String getTabela() {
		return "TeseDoutorado";
	}

	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {
		return TeseDoutorado.class;
	}

	@SuppressWarnings("unchecked")
	@Override
	protected List<TeseDoutorado> montaLista(TeseDoutorado object, Session s) {
		List<TeseDoutorado> listaRetorno = s.createQuery(
		"from Publicacao t where t.titulo like :titulo ")
			.setString("titulo", "%" + object.getTitulo() + "%")
			.list();
		return listaRetorno;
	}

	

}
