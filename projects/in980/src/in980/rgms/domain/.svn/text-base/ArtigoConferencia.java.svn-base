package in980.rgms.domain;

import java.io.PrintWriter;

import javax.persistence.Entity;
import javax.persistence.Inheritance;
import javax.persistence.InheritanceType;
import javax.persistence.PrimaryKeyJoinColumn;

@Entity
@PrimaryKeyJoinColumn(name="ID")
@Inheritance(strategy=InheritanceType.JOINED)
public class ArtigoConferencia extends Publicacao {

	private static final long serialVersionUID = 1L;
	
	private String conferencia;
	private Integer mes;
	private Integer paginas;
	

	public ArtigoConferencia(String titulo) {
		super();
		setTitulo(titulo);
	}
	
	public ArtigoConferencia() {
		super();
	}
	public String getConferencia() {
		return conferencia;
	}
	public void setConferencia(String conferencia) {
		this.conferencia = conferencia;
	}
	public Integer getMes() {
		return mes;
	}
	public void setMes(Integer mes) {
		this.mes = mes;
	}
	public Integer getPaginas() {
		return paginas;
	}
	public void setPaginas(Integer paginas) {
		this.paginas = paginas;
	}

	@Override
	public String getDescTipo() {
		return "Artigo em Conferencia";
	}
	
	public String getNomeDescritivo() {
		return "artigoConferencia";
	}

	@Override
	protected void validateSubToPersist() throws Exception{
		if(getConferencia() == null)
			throw new Exception("Conferencia invalida.");
		if(getMes() > 12 || getMes()<1 )
			throw new Exception("Mes invalida (Use um mes entre 1 e 12).");		
	}

	@Override
	protected void adicionaInfoBibtex(PrintWriter saida) {
		saida.println("@conference{/citacao/todo, ");
		saida.println("author = \" "+ getStringAutoresMembros() + "," +getAutoresNaoMembros()+ "\",");
		saida.println("title = \" "+ getTitulo() +" \",");
		saida.println("booktitle = \" "+ getConferencia() +" \",");
		saida.println("year = \" "+ getAno()  +" \",");
		saida.println("month = \" "+ getMes() +" \",");
		saida.println("pages = \" "+ getPaginas() +" \",");
		saida.println("}");
	}
}
