<?xml version="1.0" encoding="UTF-8" ?>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>IN980 - RGMS</title>

<script type="text/javascript">
	function esconderFrame(frame) {
		document.getElementById ("frameArtigoPeriodico").style.visibility="hidden"
	}
</script>

</head>
<body>
	<c:if test="${artigoRevista ne null}">
		<%@include file="cadastra_artigo_revista.jsp" %>
	</c:if>
	<c:if test="${artigoConferencia ne null}">
		<%@include file="cadastra_artigo_conferencia.jsp" %>
	</c:if>
	<c:if test="${dissertacaoMestrado ne null}">
		<%@include file="cadastra_dissertacao_mestrado.jsp" %>
	</c:if>
	<c:if test="${teseDoutorado ne null}">
		<%@include file="cadastra_tese_doutorado.jsp" %>
	</c:if>
</body>
</html>