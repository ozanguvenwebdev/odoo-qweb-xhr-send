token = query_string.get('token')
log('Query String: %s' % (str(query_string)))

record = env['accommodation.request'].search([('id', '=', int(query_string['konaklama_req']))])
if record.x_token != token:
  action = {'code':404, 'message': "Erişim yetkiniz bulunmamaktadır."}
else:
  record = record.with_context(from_api=True)
  state = str(query_string['state'])
  
  is_html=True
  if state == 'positive': #Onayla'ya basınca
  
    action = '<html><head><meta charset="UTF-8"> <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"></head><body class="p-4"> <header class="alert btn-success" style="min-height:100px; margin:0;"><img src="https://***************/assets/media/svg/brand_logo_white.svg" style="max-height:80px;"/></header><section class="text-center" style="background-color:#f8f8f8; padding: 10% 0;"><div class="alert" role="alert" style="max-width:686px; background-color:white; margin:0 30%; box-shadow: 40px 40px 160px 0 rgba(0, 0, 0, 0.08), -8px 8px 15px 0 rgba(120, 120, 120, 0.04), 3px 3px 30px 0 rgba(0, 0, 0, 0.04); border: 1px solid rgba(0,0,0,.1);"> <h1 class="alert-heading text-center" style="margin-left:280px; font-size:72px; max-width:86px; border-radius:43px; color:white; background-color:#28a745;"><i>✓</i></h4><h4 class="alert-heading" id="heading">Konaklama Talebini Onayladınız</h4> <hr> <p class="mb-0">BEST Transformer</p></div></section><footer class="alert btn-success" style="min-height:50px;"></footer></body><html></html>'

    record['x_state'] = 'tamamlandi'
  
    if record.x_konaklama_yoneticisi_id.user_id:
      record.sudo().with_context(safe=True,skip_automations=True).message_post_with_template(136,
      message_type='email',
      subtype='mail.mt_comment', 
      composition_mode='comment',
      partner_ids=[(4,record.x_konaklama_yoneticisi_id.user_id.partner_id.id)],
      to_partner_ids=[(4,record.x_konaklama_yoneticisi_id.user_id.partner_id.id)],
      force_send=True)
    if record.employee_id.user_id:
      record.sudo().with_context(safe=True,skip_automations=True).message_post_with_template(136,
      message_type='email',
      subtype='mail.mt_comment', 
      composition_mode='comment',
      partner_ids=[(4,record.employee_id.user_id.partner_id.id)],
      to_partner_ids=[(4,record.employee_id.user_id.partner_id.id)],
      force_send=True)
    
    
  elif state == 'negative' and 'reason' in query_string: #Reddet
    record.with_context(reason=str(query_string['reason'])).message_post_with_template(137, message_type='email', subtype='mail.mt_comment', partner_ids=[(6,0,record.x_konaklama_yoneticisi_id.user_id.partner_id.ids)], to_partner_ids=[(6,0,record.x_konaklama_yoneticisi_id.user_id.partner_id.ids)])
    record['x_state'] = 'reddedildi'
    record['x_ret_sebebi'] = str(query_string['reason'])
  
  elif state == 'negative': #Reddetme Nedeni Girme Sayfasına Gidiş
    # record['x_state'] = 'reddedildi'
    action = '<html><head><meta charset="UTF-8"> <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"></head><body class="p-4"> <header class="alert btn-danger" style="min-height:100px; margin:0;"><img src="https://***************/assets/media/svg/brand_logo_white.svg" style="max-height:80px;"/></header><section class="text-center" style="background-color:#f8f8f8; padding: 10% 0;"><div class="alert" role="alert" style="max-width:686px; background-color:white; margin:0 30%; box-shadow: 40px 40px 160px 0 rgba(0, 0, 0, 0.08), -8px 8px 15px 0 rgba(120, 120, 120, 0.04), 3px 3px 30px 0 rgba(0, 0, 0, 0.04); border: 1px solid rgba(0,0,0,.1);"> <h1 class="alert-heading text-center" style="margin-left:280px; font-size:72px; max-width:86px; border-radius:43px; color:white; background-color:#dc3545;"><i>×</i></h4><h4 class="alert-heading" id="heading">Konaklama Talebi Reddetme</h4> <p class="d-none" id="message">Geri bildiriminiz için teşekkür ederiz.</p><p class="d-none" id="konaklama_id">'+str(record.id)+'</p><p class="d-none" id="token">'+str(record.x_token)+'</p><div class="form-group" id="reasongroup"> <label for="reason" class="col-form-label">Reddetme Nedeniniz:</label> <input required type="text" class="form-control" id="reason" placeholder="Lütfen konaklama talebi reddetme nedeninizi giriniz..."> </div><button class="btn btn-secondary" onclick="closeTab();">Kapat</button> <button class="btn btn-danger" id="negativebtn" onclick="reject();">Reddet</button> <hr> <p class="mb-0">BEST Transformer</p></div><script>function closeTab(){window.close();}function reject(){var reason=document.getElementById("reason").value; var konaklama_id=document.getElementById("konaklama_id").textContent; var token=document.getElementById("token").textContent; if (reason !==""){const xhr = new XMLHttpRequest(); xhr.open("GET", "***************/customhttp/run/konaklama_acente_onayi?konaklama_req=" + konaklama_id + "&token="+token +"&state=negative&reason=" + reason, true); xhr.send(); xhr.onreadystatechange=function (){if (xhr.readyState===4){if (xhr.status===200){console.log(xhr.responseText); document.getElementById("message").classList.remove("d-none"); document.getElementById("reasongroup").classList.add("d-none"); document.getElementById("negativebtn").classList.add("d-none"); document.getElementById("heading").textContent="Konaklama Talebi Reddedildi!";}else{console.error("İstek başarısız: " + xhr.status);}}};}else{alert("Reddetme nedeni alanı zorunludur.");}}</script></section><footer class="alert btn-danger" style="min-height:50px;"></footer></body><html></html>'
