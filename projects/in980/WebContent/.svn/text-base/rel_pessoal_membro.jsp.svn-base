<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="s" uri="/struts-tags" %>
<title>IN980 - RGMS</title>
<script type="text/javascript">
</script> 
</head>
<body>
	<h1><s:text name="lbl.toppage.bemVindoPaginaMembro">
			<s:param>${membro.nome}</s:param>
		</s:text> 
	</h1>
	${msg}
	<table border="0">
		
		<tr>				
			<td>
				<img height="200" width="250" src="${membro.caminhoRelativoImagem}" alt="" /><br/>
				${membro.email}<br/>
				${membro.fone}<br/>
				${membro.universidade}<br/>
				${membro.website}<br/>				
			</td>
		</tr>
		<tr>
			<td>
			<br/>
			<h4><s:text name="lbl.info.publicacoes"/></h4>
			</td>
		</tr>
		<c:forEach var="publicacao" items="${membro.publicacoes}">
			<tr>
				<td>
					${publicacao.titulo}
					(<a href="${publicacao.caminhoRelativoArquivo}">pdf</a>)
					(<a href="${publicacao.caminhoRelativoBibtex}">bib</a>)
				</td>
				<td>${publicacao.ano}</td>
				<td>&nbsp; ( ${publicacao.descTipo } ) &nbsp;</td>
			</tr>			
		</c:forEach>
		<tr>
			<td>
			<br/>
			<h4><s:text name="lbl.info.linhaPesquisa"/></h4>
			</td>
		</tr>
		<c:forEach var="linhaPesquisa" items="${membro.linhasPesquisa}">
			<tr>
				<td>
					${linhaPesquisa.titulo}
				</td>
				<td>
					${linhaPesquisa.descricao}
				</td>
			</tr>			
		</c:forEach>
	</table>	

	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>