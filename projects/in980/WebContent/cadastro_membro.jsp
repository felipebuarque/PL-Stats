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
		<h1><s:text name="lbl.toppage.cadastroMembro" /></h1>
	<form action="inserirMembro" method="post" name="formCadastroMembro" enctype="multipart/form-data">
		${msg}
		<table border="1">
			<tr>
				<td><s:text name="lbl.form.id" />:</td>
				<td><input type="text" name="membro.ID" size="5" maxlength="5" readonly="readonly" value="${membro.ID}" /> </td>
			</tr>
			<tr>				
				<td><s:file name="membro.upload" label="Foto"/> &nbsp;
					<c:if test="${membro.ID ne null}">
						<img height="100" width="100" src="${membro.caminhoRelativoImagem}" alt="" />
					</c:if>
				</td>
			</tr>
			
			<tr>
				<td><s:text name="lbl.form.nome" />:</td>
				<td><input type="text" name="membro.nome" size="30" value="${membro.nome}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.email" />:</td>
				<td><input type="text" name="membro.email" size="12" value="${membro.email}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.fone" />:</td>
				<td><input type="text" name="membro.fone" size="12" value="${membro.fone}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.universidade" />:</td>
				<td><input type="text" name="membro.universidade" size="30" value="${membro.universidade}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.website" />:</td>
				<td><input type="text" name="membro.website" size="30" value="${membro.website}" /> </td>
			</tr>
			<tr>
				<s:select label="Linhas de Pesquisa" 
				    name="membro.linhasPesquisa.ID"    
				    list="linhasPesquisa"
				    listKey="ID"
				    listValue="titulo"
				    multiple="true"
					size="3"
					value="%{membro.linhasPesquisa.{ID}}"
				 />						
			</tr>
			<tr>
				<td><s:text name="lbl.form.ativo" />:</td>
				<td>
					<input type="radio" name="membro.ativo" value="0" ${membro.ativo eq 0 ? 'checked' : ''}><s:text name="lbl.form.ativo" /></input>
					<input type="radio" name="membro.ativo" value="1" ${membro.ativo eq 1 ? 'checked' : ''}><s:text name="lbl.form.inativo" /></input>  
				</td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.tipoParticipacao" />:</td>
				<td>
					<input type="radio" name="membro.tipo" value="1" ${membro.tipo eq 1 ? 'checked' : ''}><s:text name="lbl.form.professor" /></input> 
					<input type="radio" name="membro.tipo" value="2" ${membro.tipo eq 2 ? 'checked' : ''}><s:text name="lbl.form.estudante" /></input>
					<input type="radio" name="membro.tipo" value="3" ${membro.tipo eq 3 ? 'checked' : ''}><s:text name="lbl.form.pesquisador" /></input>
				</td>
			</tr>
						<tr>
				<td><s:text name="lbl.form.login" />:</td>
				<td><input type="text" name="membro.usuario.login" size="30" value="${membro.usuario.login}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.senha" />:</td>
				<td><input type="password" name="membro.usuario.senha" size="8" value="${membro.usuario.senha}" /> </td>
			</tr>
												
			<tr>			
				<td>
					<input type="submit" value="Enviar" />											
				</td>
				<td><input type="reset" value="Cancelar" /></td>
			</tr>
		</table>	
	</form>		
	<br/>
	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>