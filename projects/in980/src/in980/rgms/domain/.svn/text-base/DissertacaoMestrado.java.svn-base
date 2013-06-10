package in980.rgms.domain;

import java.io.PrintWriter;

import javax.persistence.Entity;
import javax.persistence.Inheritance;
import javax.persistence.InheritanceType;
import javax.persistence.PrimaryKeyJoinColumn;

@Entity
@PrimaryKeyJoinColumn(name="ID")
@Inheritance(strategy=InheritanceType.JOINED)
public class DissertacaoMestrado extends Publicacao{

	private static final long serialVersionUID = 1L;
	private String escola;
	private Integer mes;
	
	
	public DissertacaoMestrado(String titulo) {
		setTitulo(titulo);
	}
	
	public DissertacaoMestrado() {
		super();
	}
	public String getEscola() {
		return escola;
	}
	public void setEscola(String escola) {
		this.escola = escola;
	}
	
	@Override
	public String getDescTipo() {
		return "Dissertacao de Mestrado";
	}
	@Override
	public String getNomeDescritivo() {
		return "dissertacaoMestrado";
	}
	public Integer getMes() {
		return mes;
	}
	public void setMes(Integer mes) {
		this.mes = mes;
	}
	
	@Override
	protected void validateSubToPersist() throws Exception{
		if(getEscola() == null)
			throw new Exception("Escola invalida.");
		if(getMes() > 12 || getMes()<1 )
			throw new Exception("Mes invalida (Use um mes entre 1 e 12).");
	}
	
	@Override
	protected void adicionaInfoBibtex(PrintWriter saida) {
		saida.println("@mastersthesis{/citacao/todo, ");
		saida.println("author = \" "+ getStringAutoresMembros() +" \",");
		saida.println("title = \" "+ getTitulo() +" \",");
		saida.println("school = \" "+ getEscola() +" \",");
		saida.println("year = \" "+ getAno()  +" \",");
		saida.println("month = \" "+ getMes() +" \",");
		saida.println("}");
		
	}
}
