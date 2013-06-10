package in980.rgms.domain;

import java.io.PrintWriter;

import javax.persistence.Entity;
import javax.persistence.Inheritance;
import javax.persistence.InheritanceType;
import javax.persistence.PrimaryKeyJoinColumn;

@Entity
@PrimaryKeyJoinColumn(name="ID")
@Inheritance(strategy=InheritanceType.JOINED)
public class ArtigoRevista extends Publicacao{

	private static final long serialVersionUID = 1L;
	
	private String journal;
	private Integer volume;
	private Integer paginas;
	private String numero;
	
	
	public ArtigoRevista(String tituloPublicacao) {
		setTitulo(tituloPublicacao);
	}
	
	public ArtigoRevista() {
		super();
	}
	
	
	
	public String getJournal() {
		return journal;
	}
	public void setJournal(String journal) {
		this.journal = journal;
	}
	public Integer getVolume() {
		return volume;
	}
	public void setVolume(Integer volume) {
		this.volume = volume;
	}
	public Integer getPaginas() {
		return paginas;
	}
	public void setPaginas(Integer paginas) {
		this.paginas = paginas;
	}
	public String getNumero() {
		return numero;
	}
	public void setNumero(String numero) {
		this.numero = numero;
	}

	@Override
	public String getDescTipo() {
		return "Artigo em Revista/Periodico";
	}
	
	public String getNomeDescritivo() {
		return "artigoRevista";
	}
	
	@Override
	protected void validateSubToPersist() throws Exception{
		if(getJournal() == null)
			throw new Exception("Journal invalida.");		
	}
	
	@Override
	protected void adicionaInfoBibtex(PrintWriter saida) {
		saida.println("@article{/citacao/todo, ");
		saida.println("author = \" "+ getStringAutoresMembros() +" \",");
		saida.println("title = \" "+ getTitulo() +" \",");
		saida.println("journal = \" "+ getJournal() +" \",");
		saida.println("year = \" "+ getAno()  +" \",");
		saida.println("volume = \" "+ getVolume() +" \",");
		saida.println("number = \" "+ getNumero() +" \",");
		saida.println("pages = \" "+ getPaginas() +" \",");
		saida.println("}");
	}

}
