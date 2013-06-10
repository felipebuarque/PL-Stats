<?xml version="1.0" encoding="UTF-8" ?>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="s" uri="/struts-tags" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>IN980 - RGMS</title>

</head>
<body>
	<h1><s:text name="lbl.toppage.cadastroArtigoRevista"/></h1>
	<form action="inserirArtigoRevista" name="formInserirArtigoRevista" method="post" enctype="multipart/form-data">
		${msg}
		<table border="1">
			<tr>
				<td><s:text name="lbl.form.id" />:</td>
				<td><input type="text" name="artigoRevista.ID" size="5" maxlength="5" readonly="readonly" value="${artigoRevista.ID}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.titulo" />:</td>
				<td><input type="text" name="artigoRevista.titulo" size="100" value="${artigoRevista.titulo}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.journal" />:</td>
				<td><input type="text" name="artigoRevista.journal" size="80" value="${artigoRevista.journal}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.ano" />:</td>
				<td><input type="text" name="artigoRevista.ano" size="4" maxlength="4" value="${artigoRevista.ano}" /> </td>
			</tr>			
			<tr>
			<td><s:text name="lbl.form.volume" />:</td>
				<td><input type="text" name="artigoRevista.volume" size="4" maxlength="4" value="${artigoRevista.volume}" /> </td>
			</tr>
			<tr>
			<td><s:text name="lbl.form.numero" />:</td>
				<td><input type="text" name="artigoRevista.numero" size="4" value="${artigoRevista.numero}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.pagina" />:</td>
				<td><input type="text" name="artigoRevista.paginas" size="3" maxlength="3" value="${artigoRevista.paginas}" /> </td>
			</tr>
			<tr>
				<s:select label="Autores Membros" 
				    name="artigoRevista.autoresMembros.ID"    
				    list="membros"
				    listKey="ID"
				    listValue="nome"
				    multiple="true"
					size="3"
					value="%{artigoRevista.autoresMembros.{ID}}"
				 />
						
			</tr>
			<tr>
				<td><s:text name="lbl.form.autoresNaoMembros" />*:</td>
				<td>
					<input type="text" name="artigoRevista.autoresNaoMembros" value="" />
				</td>
			</tr>
			<tr>
				<s:select label="Linhas de Pesquisa" 
				    name="artigoRevista.linhasPesquisa.ID"    
				    list="linhasPesquisa"
				    listKey="ID"
				    listValue="titulo"
				    multiple="true"
					size="3"
					value="%{artigoRevista.linhasPesquisa.{ID}}"
				 />
						
			</tr>
			<tr>
				<td>
					<s:file name="artigoRevista.upload" label="Arquivo"/> &nbsp;					
				</td>
			</tr>
			<tr>
				<td><input type="submit" value="<s:text name="lbl.btn.enviar" />" /> </td>
				<td><input type="reset" value="<s:text name="lbl.btn.cancelar" />" /></td>
			</tr>
		</table>	
	</form>
	<br/>
	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>