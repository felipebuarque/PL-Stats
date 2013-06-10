package in980.rgms.persistence;

import in980.rgms.domain.ArtigoRevista;

import java.util.List;

import org.hibernate.Session;

public class ArtigoRevistaDAO extends Dao<ArtigoRevista>{

	@Override
	protected String getTabela() {
		return "ArtigoRevista";
	}

	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {		
		return ArtigoRevista.class;
	}

	@SuppressWarnings("unchecked")
	@Override
	protected List<ArtigoRevista> montaLista(ArtigoRevista object, Session s) {
		List<ArtigoRevista> listaRetorno = s.createQuery(
				"from Publicacao t where t.titulo like :titulo ")
			.setString("titulo", "%" + object.getTitulo() + "%")
			.list();
		return listaRetorno;
	}

	

}
