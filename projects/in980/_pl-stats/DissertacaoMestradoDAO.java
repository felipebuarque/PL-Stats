package in980.rgms.persistence;

import in980.rgms.domain.DissertacaoMestrado;

import java.util.List;

import org.hibernate.Session;

public class DissertacaoMestradoDAO extends Dao<DissertacaoMestrado>{

	@Override
	protected String getTabela() {
		return "DissertacaoMestrado";
	}

	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {
		return DissertacaoMestrado.class;
	}

	@SuppressWarnings("unchecked")
	@Override
	protected List<DissertacaoMestrado> montaLista(DissertacaoMestrado object,
			Session s) {
		List<DissertacaoMestrado> listaRetorno = s.createQuery(
		"from Publicacao t where t.titulo like :titulo ")
			.setString("titulo", "%" + object.getTitulo() + "%")
			.list();
		return listaRetorno;
	}

	
}
