<%!
    import time
    import pylowiki.lib.db.event            as eventLib
    import pylowiki.lib.db.workshop         as workshopLib
    import pylowiki.lib.db.account          as accountLib
%>  

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="manage_account()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Manage Your Professional Workshop Account</h4>
                <div class="row-fluid">
                    <div class="span1">
                    </div>
                    <div class="span11">
                        <div class="well">
                            <strong>Udate Billing Contact Information</strong><br />
                            <form name="updateBillingContact" id="updateBillingContact" class="left form-inline" action = "/account/${c.account['urlCode']}/update/billingContact/handler" enctype="multipart/form-data" method="post" >
                                <strong>Billing Name:</strong> <input type="text" name="billingName" value="${c.account['billingName']}"><br />
                                <strong>Billing Email:</strong> <input type="text" name="billingEmail" value="${c.account['billingEmail']}"><br /><br />
                                <button type="submit" class="btn btn-warning">Save Changes</button>
                            </form>
                        </div><!--- well -->
                        <div class="well">
                            <strong>Update Credit Card Information</strong><br />
                            <form action="/account/${c.account['urlCode']}/update/paymentInfo/handler" method="post" id="paymentForm">
                                <div class="form-row">
                                    <label>Credit Card Number (use 4242424242424242 for testing)</label>
                                    <input type="text" maxlength="20" autocomplete="off" class="card-number stripe-sensitive required" />
                                </div><!-- form-row -->
                                <div class="form-row">
                                    <label>CVC</label>
                                    <input type="text" maxlength="4" autocomplete="off" class="card-cvc stripe-sensitive required" />
                                </div><!-- form-row -->
                                <div class="form-row">
                                    <label>Expiration</label>
                                    <div class="expiry-wrapper">
                                        <select class="card-expiry-month stripe-sensitive required">
                                        </select>
                                        <script type="text/javascript">
                                            var select = $(".card-expiry-month"),
                                            month = new Date().getMonth() + 1;
                                            for (var i = 1; i <= 12; i++) {
                                                select.append($("<option value='"+i+"' "+(month === i ? "selected" : "")+">"+i+"</option>"))
                                            }
                                        </script>
                                        <span> / </span>
                                        <select class="card-expiry-year stripe-sensitive required"></select>
                                        <script type="text/javascript">
                                            var select = $(".card-expiry-year"),
                                            year = new Date().getFullYear();
                                            for (var i = 0; i < 12; i++) {
                                                select.append($("<option value='"+(i + year)+"' "+(i === 0 ? "selected" : "")+">"+(i + year)+"</option>"))
                                            }
                                        </script>
                                    </div><!-- expiry-wrapper -->
                                </div><!-- form-row -->
                                <div class="form-row">
                                    <button type="submit" name="submit-button" class="btn btn-warning">Save Changes</button>
                                </div><!-- form-row -->
                            </form>
                        </div><!-- well -->
                            <form name="updateBillingContact" id="updateBillingContact" class="left form-inline" action = "/account/${c.account['urlCode']}/cancel/handler" enctype="multipart/form-data" method="post" >
                                <div class="accordion well" id="accordion2">
                                    <div class="accordion-group">
                                        <div class="accordion-heading" style="text-align: center">
                                            <button type="button" class="btn btn-danger" data-toggle="collapse" data-target="#collapseOne">
                                                Close Account
                                            </button>
                                        </div><!-- accordion-heading -->
                                        <div id="collapseOne" class="accordion-body collapse">
                                            <div class="accordion-inner" style="text-align: center">
                                            Are you sure? This will close your Civinomics account and remove your workshop from the system.<br /><br />
                                            <button type="submit" name="confirmCancel" class="btn btn-danger">Confirm Account Close</button> &nbsp; &nbsp;
                                            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#collapseOne">
                                            Oops! Never mind!
                                            </button>
                                            </div><!-- accordian-inner -->
                                        </div><!-- accordion-body -->
                                    </div><!-- accordion-group -->
                                </div><!-- accordian -->
                            </form>
                    </div><!-- span11 -->
                </div><!-- row-fluid -->
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="show_invoices()">
    <%
        numInvoices = c.accountInvoices['count']
        invoiceList = c.accountInvoices['data']
    %>
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Account Invoices</h4>
            <div class="row-fluid">
                <div class="span1">
                </div>
                <div class="span11">
                    Total Invoices: ${numInvoices}<br />
                    <ul>
                    % for invoice in invoiceList:
                        ${display_invoice(invoice)}
                    % endfor
                    </ul>
                </div><!-- span11 -->
            </div><!-- row-fluid -->
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="display_invoice(invoice)">
    <li><strong>Date: </strong> ${time.ctime(invoice['date'])} Amount Due: ${invoice['amount_due']/100} Paid: 
    % if invoice['ending_balance'] == 0:
        Yes
    % else:
        No ${invoice}
    % endif
    Line items:
    <ol>
    % for line in invoice['lines']['data']:
        <li>${line['plan']['name']} for period of ${time.ctime(line['period']['start'])} through ${time.ctime(line['period']['end'])}</li>
    % endfor
    </ol>
    </li>
</%def>

<%def name="show_events()">
    <div class="row-fluid">
        <div class="section-wrapper">
            <div class="browse">
                <h4 class="section-header" style="text-align: center"><br />Event Log</h4>
                A record of configuration and administrative changes to the account.<br />
                <% aEvents = eventLib.getParentEvents(c.account) %>
                <table class="table table-bordered">
                <thead>
                <tr><th>Account Events</th></tr>
                </thead>
                <tbody>
                % if aEvents:
                    <br /><br />
                    % for aE in aEvents:
                        <tr><td><strong>${aE.date} ${aE['title']}</strong> ${aE['data']}</td></tr>
                    % endfor
                % endif
                </tbody>
                </table>
            </div><!-- browse -->
        </div><!-- section-wrapper -->
    <div><!-- row-fluid -->
</%def>

