log('params : %s' % str(params))


def create_attachment(file,applicant_id,document_type):
  # TODO: res_id yi qweb'ten yolla ve burada al | şimdilik örnek olarak 101 id'sini kullanıyoruz.
  if file:
    created_file = env['ir.attachment'].create({
      'type'        : 'binary',
      'name'        : file.filename,
      'datas_fname' : file.filename,
      'datas'       : base64.b64encode(file.read()),
      'res_model'   : 'accommodation.request',
      'res_id'      : konaklama_id,
    })
    log('new file added to ir.attachment model. name: %s id: %s' % (created_file.name, created_file.id))
    
is_html = False

expected_files = [
 'konaklama_belge',
]

try:
  konaklama_id = params.get('konaklama_id')
  results = []

  for expected_file in expected_files:
    file_data = request.httprequest.files.getlist(expected_file)
    if file_data:
      for file in file_data:
        create_attachment(file, konaklama_id, expected_file)
      results.append(expected_file)
  
  applicant = env['accommodation.request'].browse(int(konaklama_id))
  
  action = {'message':'ok', 'code':200}
  
  
except Exception as error:
  log(str(error))
  action = {'message':str(error), 'code':500}
