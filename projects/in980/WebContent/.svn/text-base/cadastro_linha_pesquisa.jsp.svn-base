<?xml version="1.0" encoding="UTF-8" ?>
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="s" uri="/struts-tags"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>IN980 - RGMS</title>


</head>
<body>
<h1><s:text name="lbl.toppage.cadastroLinhaPesquisa" /></h1>
<form action="inserirLinhaPesquisa" name="formInserirLinhaPesquisa"
	method="post">${msg}
<table border="1">
	<tr>
		<td><s:text name="lbl.form.id" />:</td>
		<td><input type="text" name="linhaPesquisa.ID" size="5"
			maxlength="5" readonly="readonly" value="${linhaPesquisa.ID}" /></td>
	</tr>
	<tr>
		<td><s:text name="lbl.form.titulo" />*:</td>
		<td><input type="text" name="linhaPesquisa.titulo" size="100"
			value="${linhaPesquisa.titulo}" /></td>
	</tr>
	<tr>
		<td><s:text name="lbl.form.descricao" />*:</td>
		<td><input type="text" name="linhaPesquisa.descricao" size="80"
			value="${linhaPesquisa.descricao}" /></td>
	</tr>
	<tr>
		<td><s:text name="lbl.form.descricaoDetalhada" />:</td>
		<td><input type="text" name="linhaPesquisa.descricaoDetalhada"
			size="100" maxlength="200"
			value="${linhaPesquisa.descricaoDetalhada}" /></td>
	</tr>
	<tr>
		<td><s:text name="lbl.form.financiadores" />:</td>
		<td><input type="text" name="linhaPesquisa.financiadores"
			size="100" maxlength="100" value="${linhaPesquisa.financiadores}" />
		</td>
	</tr>
	<tr>
		<td><s:text name="lbl.form.links" />:</td>
		<td><input type="text" name="linhaPesquisa.links" size="80"
			value="${linhaPesquisa.links}" /></td>
	</tr>
	<tr>
		<s:select label="Membros" name="linhaPesquisa.membros.ID"
			list="membros" listKey="ID" listValue="nome" multiple="true" size="3"
			value="%{linhaPesquisa.membros.{ID}}">
			

		</s:select>
	</tr>
	<tr>
			<s:select label="Publicações" name="linhaPesquisa.publicacoes.ID"
				list="publicacoes" listKey="ID" listValue="titulo" multiple="true" size="3"
				value="%{publicacoes.{ID}}">
			</s:select>		
	</tr>
	<tr>
		<td><input type="submit" value="<s:text name="lbl.btn.enviar" />" />
		</td>
		<td><input type="reset"
			value="<s:text name="lbl.btn.cancelar" />" /></td>
	</tr>
</table>
</form>
<br />
<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>