package in980.rgms.persistence;

import in980.rgms.domain.ArtigoConferencia;

import java.util.List;

import org.hibernate.Session;

public class ArtigoConferenciaDAO extends Dao<ArtigoConferencia>{

	
	@Override
	protected String getTabela() {
		return "ArtigoConferencia";
	}


	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {
		return ArtigoConferencia.class;
	}


	@SuppressWarnings("unchecked")
	@Override
	protected List<ArtigoConferencia> montaLista(ArtigoConferencia object, Session s) {
		List<ArtigoConferencia> listaRetorno = s.createQuery(
		"from Publicacao t where t.titulo like :titulo")
			.setString("titulo", "%" + object.getTitulo() + "%")
			.list();
		return listaRetorno;
	}

}
