package in980.rgms.presentation;

import in980.rgms.utils.HibernateUtils;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hibernate.SessionFactory;
import org.hibernate.StaleObjectStateException;

/**
 * Servlet Filter implementation class OpenSessionFilter
 */
public class OpenSessionFilter implements Filter {

	private static Log log = LogFactory.getLog(OpenSessionFilter.class);
	private SessionFactory sf;

	/**
	 * Default constructor.
	 */
	public OpenSessionFilter() {
		// TODO Auto-generated constructor stub
	}

	/**
	 * @see Filter#destroy()
	 */
	public void destroy() {
		// TODO Auto-generated method stub
	}

	/**
	 * @see Filter#doFilter(ServletRequest, ServletResponse, FilterChain)
	 */
	public void doFilter(ServletRequest request, ServletResponse response,
			FilterChain chain) throws IOException, ServletException {
		try {
			// place your code here
			log.debug("Starting a database transaction");
			sf.getCurrentSession().beginTransaction();
			// pass the request along the filter chain
			chain.doFilter(request, response);
			// After
			log.debug("Committing the database transaction");
			sf.getCurrentSession().getTransaction().commit();
		} catch (StaleObjectStateException staleEx) {
			log.error("This interceptor does not implement optimistic concurrency control!");
			log.error("Your application will not work until you add compensation actions!");
			// Rollback, close everything, possibly compensate for any permanent
			// changes  during the conversation, and finally restart business
			// conversation. Maybe give the user of the application a chance to merge some of his
			// work with fresh data... what you do here depends on your applications
			// design.
			throw staleEx;
		} catch (Throwable ex) {
			// Rollback only
			ex.printStackTrace();
			try {
				if (sf.getCurrentSession().getTransaction().isActive()) {
					log.debug("Trying to rollback database transaction after exception");
					sf.getCurrentSession().getTransaction().rollback();
				}
			} catch (Throwable rbEx) {
				log.error("Could not rollback transaction after exception!",
						rbEx);
			}

			// Let others handle it... maybe another interceptor for exceptions?
			throw new ServletException(ex);
		}
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	public void init(FilterConfig fConfig) throws ServletException {
		log.debug("Initializing filter...");
		log.debug("Obtaining SessionFactory from static HibernateUtil singleton");
		sf = HibernateUtils.getSessionFactory();
	}

}
