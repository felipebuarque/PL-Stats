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
	<h1><s:text name="lbl.toppage.cadastroArtigoConferencia"/></h1>
	<form action="inserirArtigoConferencia" name="formInserirArtigoConferencia" method="post" enctype="multipart/form-data" >
		${msg}
		<table border="1">
			<tr>
				<td><s:text name="lbl.form.id" />:</td>
				<td><input type="text" name="artigoConferencia.ID" size="5" maxlength="5" readonly="readonly" value="${artigoConferencia.ID}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.titulo" />:</td>
				<td><input type="text" name="artigoConferencia.titulo" size="100" value="${artigoConferencia.titulo}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.conferencia" />:</td>
				<td><input type="text" name="artigoConferencia.conferencia" size="80" value="${artigoConferencia.conferencia}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.ano" />:</td>
				<td><input type="text" name="artigoConferencia.ano" size="4" maxlength="4" value="${artigoConferencia.ano}" /> </td>
			</tr>			
			<tr>
				<td><s:text name="lbl.form.mes" />:</td>
				<td><input type="text" name="artigoConferencia.mes" size="2" value="${artigoConferencia.mes}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.pagina" />:</td>
				<td><input type="text" name="artigoConferencia.paginas" size="3" maxlength="3" value="${artigoConferencia.paginas}" /> </td>
			</tr>
			<tr>
				<s:select label="Autores Membros" 
				    name="artigoConferencia.autoresMembros.ID"    
				    list="membros"
				    listKey="ID"
				    listValue="nome"
				    multiple="true"
				    size="3"
				    value="%{artigoConferencia.autoresMembros.{ID}}"
				 />
				 		
			</tr>
			<tr>
				<td><s:text name="lbl.form.autoresNaoMembros" />*:</td>
				<td>
					<input type="text" name="artigoConferencia.autoresNaoMembros" value="${artigoConferencia.autoresNaoMembros}" />
				</td>
			</tr>
			<tr>
				<s:select label="Linhas de Pesquisa" 
				    name="artigoConferencia.linhasPesquisa.ID"    
				    list="linhasPesquisa"
				    listKey="ID"
				    listValue="titulo"
				    multiple="true"
					size="3"
					value="%{artigoConferencia.linhasPesquisa.{ID}}"
				 />
						
			</tr>
			<tr>
				<td>
					<s:file name="artigoConferencia.upload" label="Arquivo"/> &nbsp;					
				</td>
			</tr>
			<tr>
				<td><input type="submit" value="<s:text name="lbl.btn.enviar" />" /> </td>
				<td><input type="reset" value="<s:text name="lbl.btn.cancelar" />" /></td>
			</tr>
		</table>	
	</form>
	<h6>*<s:text name="msg.separePorVirgula" /></h6>
	<br/>
	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>