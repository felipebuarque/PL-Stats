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
	<h1><s:text name="lbl.toppage.cadastroTeseDoutorado"/></h1>
	<form action="inserirTeseDoutorado" name="formInserirTeseDoutorado" method="post" enctype="multipart/form-data">
		${msg}
		<table border="1" >
			<tr>
				<td><s:text name="lbl.form.id" />:</td>
				<td><input type="text" name="teseDoutorado.ID" size="5" maxlength="5" readonly="readonly" value="${teseDoutorado.ID}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.titulo" />:</td>
				<td><input type="text" name="teseDoutorado.titulo" size="100" value="${teseDoutorado.titulo}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.escola" />:</td>
				<td><input type="text" name="teseDoutorado.escola" size="80" value="${teseDoutorado.escola}" /> </td>
			</tr>
			<tr>
				<td><s:text name="lbl.form.ano" />:</td>
				<td><input type="text" name="teseDoutorado.ano" size="4" maxlength="4" value="${teseDoutorado.ano}" /> </td>
			</tr>			
			<tr>
			<td><s:text name="lbl.form.mes" />:</td>
				<td><input type="text" name="teseDoutorado.mes" size="2" maxlength="2" value="${teseDoutorado.mes}" /> </td>
			</tr>
			<tr>
				<td>
					<s:select label="Autores Membros"
					    name="teseDoutorado.autoresMembros.ID"    
					    list="membros"
					    listKey="ID"
					    listValue="nome"
					    multiple="true"
						size="3"
						value="%{teseDoutorado.autoresMembros.{ID}}"
					/>
				 </td>				 						
			</tr>
			<tr>
				<td><s:text name="lbl.form.autoresNaoMembros" />*:</td>
				<td>
					<input type="text" name="artigoConferencia.autoresNaoMembros" value="${teseDoutorado.autoresNaoMembros}" />
				</td>
			</tr>
			<tr>
				<s:select label="Linhas de Pesquisa" 
				    name="teseDoutorado.linhasPesquisa.ID"    
				    list="linhasPesquisa"
				    listKey="ID"
				    listValue="titulo"
				    multiple="true"
					size="3"
					value="%{teseDoutorado.linhasPesquisa.{ID}}"
				 />						
			</tr>
			<tr>
				<td>
					<s:file name="teseDoutorado.upload" label="Arquivo" >
					</s:file> &nbsp;					
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